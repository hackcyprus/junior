from .models import Team


class TeamExtractionMiddleware(object):
    """Checks the cookies for a team token, fetches the team from the database
    and puts a `team` attribute on the request object.

    """
    def process_request(self, request):
        try:
            team_token = request.get_signed_cookie('jhteam')
            if team_token:
                team = Team.objects.get(token=team_token)
                request.team = team
        except (Team.DoesNotExist, KeyError):
            pass