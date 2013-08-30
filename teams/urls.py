from django.conf.urls import patterns, url
from .views import create_team, team_created_successfully


urlpatterns = patterns('teams',
    url(r'new/$', create_team, name='create-team'),
    url(r'created/$', team_created_successfully, name='team-created')
)
