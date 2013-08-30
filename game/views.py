import json
from django.http import HttpResponse
from django.shortcuts import render


class JsonResponse(HttpResponse):
    def __init__(self, content, status_code=200):
        content = json.dumps(content)
        super(JsonResponse, self).__init__(content=content, status_code=status_code)


def team_token_required(fn):
    """Decorator for checking that requests to the decorated endpoint contain
    a team property, meaning that a team has been registered on this browser.

    """
    def wrapper(*args, **kwargs):
        request = args[0]
        if hasattr(request, 'team') and request.team:
            return fn(*args, **kwargs)
        else:
            content = {
                'error': 'You need to register a team to perform this action.'
            }
            return JsonResponse(content=content, status_code=403)
    return wrapper


def view_map(request):
    return render(request, 'game/map.html')


@team_token_required
def view_stage(request, stage_id):
    pass


@team_token_required
def skip_stage(request):
    pass


@team_token_required
def submit_solution(request):
    pass
