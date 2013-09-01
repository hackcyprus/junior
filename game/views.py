import json
from datetime import datetime
from functools import wraps

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.functional import curry
from django.utils.timezone import now

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


def view_map(request):
    problems, teams, bootstrap = [], [], {}
    for problem in Problem.objects.all().order_by('order'):
        problems.append({
            'id': problem.id,
            'name': problem.name,
            'order': problem.order
        })
    for team in Team.objects.all():
        teams.append({
            'id': team.id,
            'name': team.name,
            'position': team.latest_stage.problem.order,
            'points': team.total_points
        })
    bootstrap['problems'] = problems
    bootstrap['teams'] = teams
    if request.team:
        bootstrap['stages'] = [
            stage.to_dict() for stage in Stage.objects.filter(team=request.team)
        ]
    return render(request, 'game/map.html', {'bootstrap': dumps(bootstrap)})


@team_token_required
@valid_stage
def view_stage(request, stage_id):
    stage = Stage.objects.get(pk=int(stage_id))
    problem = stage.problem
    content = {
        'name': problem.name,
        'order': problem.order,
        'description': problem.description,
        'io_description': problem.io_description,
        'multiplier': problem.multiplier,
        'sample_in': problem.sample_in,
        'sample_out': problem.sample_out
    }
    return JsonResponse(content=content)


@team_token_required
@valid_stage
def download_test_file(request, stage_id):
    # NOTE: this is an inefficient way of serving media files, but it will do
    # for our purposes.
    stage = Stage.objects.get(pk=int(stage_id))
    filename = "problem{}.in".format(stage.problem.order)
    response = HttpResponse(stage.problem.in_file.read(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response


@team_token_required
@valid_stage
def skip_stage(request, stage_id):
    pass


@team_token_required
@valid_stage
def submit_stage(request, stage_id):
    # TODO: this method is a stub for now.
    stage = Stage.objects.get(pk=int(stage_id))
    problem = stage.problem
    game = stage.problem.game
    content = {}

    if not game.started:
        return JsonResponse(content='The game has not started yet.', status=403)

    checker = Checker()
    correct = checker.check_solution()
    content['correct'] = correct

    if correct:
        minutes_from_start = (now() - game.started_on).seconds / 60
        points = int(max(0, (problem.base_points * problem.multiplier) - minutes_from_start))
        content['points'] = points
        stage.points_earned = points
        # TODO: change this to a `state` instead.
        stage.solved = True
        stage.save()

    attempt = Attempt(correct=correct, stage=stage)
    attempt.save()

    next_stage = stage.next
    if next_stage:
        next_stage.unlock()

    return JsonResponse(content=content)
