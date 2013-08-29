from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from .forms import TeamForm
from .models import Team, Participant


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
            return redirect(reverse('team-created'))
    return render(request, 'teams/new.html', {'form': form})