import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.functional import curry

from .models import Stage, Problem
from teams.models import Team


dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
dumps = curry(json.dumps, default=dthandler)


class JsonResponse(HttpResponse):
    def __init__(self, content, status=200):
        content = json.dumps(content)
        super(JsonResponse, self).__init__(
            content,
            status=status,
            content_type='application/javascript; charset=utf8'
        )


def team_token_required(fn):
    """Decorator for checking that requests to the decorated endpoint contain
    a team property, meaning that a team has been registered on this browser.

    """
    def wrapper(*args, **kwargs):
        request = args[0]
        if hasattr(request, 'team') and request.team:
            return fn(*args, **kwargs)
        else:
            return JsonResponse(
                content='You need to register a team to perform this action.',
                status=403
            )
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
def view_stage(request, stage_id):
    try:
        stage = Stage.objects.get(pk=int(stage_id), team=request.team)
        if stage.locked:
            return JsonResponse(content='This stage is locked.', status=403)
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
    except Stage.DoesNotExist:
        return JsonResponse(content='Stage not found.', status=404)


@team_token_required
def skip_stage(request):
    pass


@team_token_required
def submit_stage(request):
    pass
