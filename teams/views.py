from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from .forms import TeamForm
from .models import Team, Participant

NINE_HOURS = 9 * 3600

def create_team(request):
    if request.method == 'GET':
        form = TeamForm()
    else:
        form = TeamForm(request.POST)
        if form.is_valid():
            team = Team(name=form.cleaned_data['name'])
            team.save()
            for name in form.cleaned_data['participants']:
                participant = Participant(name=name, team=team)
                participant.save()
            response = redirect(reverse('team-created'))
            response.set_signed_cookie('jhteam', team.token, max_age=NINE_HOURS)
            return response

    return render(request, 'teams/new.html', {'form': form})