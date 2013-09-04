from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from lib.sync import pusher
from game.models import Problem, Stage
from .forms import TeamForm
from .models import Team, Participant


NINE_HOURS = 9 * 3600


def initialize_stages(team):
    for i, problem in enumerate(Problem.objects.all().order_by('order')):
        stage = Stage(problem=problem, team=team)
        if i == 0:
            stage.unlock(save=False)
        stage.save()


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
            initialize_stages(team)
            request.session['team_name'] = team.name
            request.session['team_token'] = team.token
            response = redirect(reverse('team-created'))
            response.set_signed_cookie('jhteam', team.token, max_age=NINE_HOURS)
            pusher['updates'].trigger('team:new', team.to_dict())
            return response
    return render(request, 'teams/new.html', {'form': form})


def team_created_successfully(request):
    context = {}
    if 'team_name' in request.session:
        context['team_name'] = request.session['team_name']
        del request.session['team_name']
    if 'team_token' in request.session:
        context['team_token'] = request.session['team_token']
        del request.session['team_token']
    return render(request, 'teams/created.html', context)

