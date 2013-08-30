from .models import Team


class TeamExtractionMiddleware(object):
    """Checks the cookies for a team token, fetches the team from the database
    and puts a `team` attribute on the request object.

    """
    def process_request(self, request):
        team_token = request.COOKIES.get('jhteam')
        if team_token:
            try:
                team = Team.objects.get(token=team_token)
                request.team = team
            except Team.DoesNotExist:
                pass