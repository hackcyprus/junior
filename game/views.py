import json
import operator
from datetime import datetime
from functools import wraps

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.functional import curry
from django.utils.timezone import now

from lib.sync import pusher
from .models import Stage, Problem, Attempt
from .checker import Checker
from teams.models import Team


dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
dumps = curry(json.dumps, default=dthandler)


class JsonResponse(HttpResponse):
    def __init__(self, content, status=200):
        content = json.dumps(content)
        super(JsonResponse, self).__init__(
            content,
            status=status,
            content_type='application/json; charset=utf8'
        )


def team_token_required(fn):
    """Decorator for checking that requests to the decorated endpoint contain
    a team property, meaning that a team has been registered on this browser.

    """
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if hasattr(request, 'team') and request.team:
            return fn(request, *args, **kwargs)
        else:
            return JsonResponse(
                content='You need to register a team to perform this action.',
                status=403
            )
    return wrapper


def valid_stage(fn):
    """Decorator for checking that the requested stage exists and is unlocked
    for the currently active team. Expects the `request` object to have a `team`
    property.

    """
    @wraps(fn)
    def wrapper(request, stage_id, *args, **kwargs):
        try:
            stage = Stage.objects.get(pk=int(stage_id), team=request.team)
            if stage.locked:
                return JsonResponse(content='This stage is locked.', status=403)
            return fn(request, stage_id, *args, **kwargs)
        except Stage.DoesNotExist:
            return JsonResponse(content='Stage not found.', status=404)
    return wrapper


@team_token_required
def view_map(request):
    bootstrap = {
        'problems': [p.to_dict() for p in Problem.objects.all()],
        'teams': [t.to_dict() for t in Team.objects.all()],
        'stages': [s.to_dict() for s in Stage.objects.filter(team=request.team)]
    }
    return render(request, 'game/map.html', {'bootstrap': dumps(bootstrap)})


@team_token_required
@valid_stage
def view_stage(request, stage_id):
    stage = Stage.objects.get(pk=int(stage_id))
    problem = stage.problem
    content = {
        'stage_id': stage.id,
        'name': problem.name,
        'order': problem.order,
        'io_description': problem.io_description,
        'sample_in': problem.sample_in,
        'sample_out': problem.sample_out
    }
    return JsonResponse(content=content)


@team_token_required
@valid_stage
def download_description(request, stage_id, lang):
    # NOTE: this is an inefficient way of serving media files, but it will do
    # for our purposes.
    stage = Stage.objects.get(pk=int(stage_id))
    problem = stage.problem
    pdf = problem.pdf_gr if lang == 'gr' else problem.pdf_en
    filename = "problem{}_{}.pdf".format(problem.order, lang)
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    pdf.close()
    return response


@team_token_required
@valid_stage
def download_test_file(request, stage_id):
    # NOTE: Same as above.
    stage = Stage.objects.get(pk=int(stage_id))
    problem = stage.problem
    in_file = problem.in_file
    filename = "problem{}.in".format(problem.order)
    response = HttpResponse(in_file.read(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    in_file.close()
    return response


@team_token_required
@valid_stage
def skip_stage(request, stage_id):
    pass


@team_token_required
@valid_stage
def submit_stage(request, stage_id):
    stage = Stage.objects.get(pk=int(stage_id))
    problem = stage.problem
    game = stage.problem.game
    content = {}

    if not game.started:
        return JsonResponse(content='The game has not started yet.', status=403)

    pusher['updates'].trigger('submission:start', {'team_id': request.team.id})

    solution = request.POST.get('solution')

    checker = Checker(problem)
    correct = checker.check_solution(solution)
    state = Stage.SOLVED_CORRECTLY if correct else Stage.TRIED_BUT_FAILED
    if correct:
        minutes_from_start = (now() - game.started_on).seconds / 60
        points = int(max(0, (problem.base_points * problem.multiplier) - minutes_from_start))
    else:
        points = 0
    stage.points_earned = points
    stage.state = state
    stage.save()

    content['stage_points'] = points
    content['team_points'] = request.team.total_points
    content['state'] = state

    attempt = Attempt(correct=correct, stage=stage, solution=solution)
    attempt.save()

    next_stage = stage.next
    new_position = None
    if correct and next_stage and next_stage.locked:
        next_stage.unlock()
        new_position = next_stage.problem.order

    pusher['updates'].trigger('submission:finish', {
        'team_id': request.team.id,
        'team_points': content['team_points'],
        'problem_order': problem.order,
        'new_position': new_position,
        'state': content['state']
    })

    return JsonResponse(content=content)


def leaderboard(request):
    board = []
    for team in Team.objects.all():
        stats = team.attempt_stats()
        board.append((team.name, sum(stats)) + stats + (team.total_points,))
    return render(request, 'game/leaderboard.html', {
        'board': sorted(board, reverse=True, key=operator.itemgetter(6))
    })
