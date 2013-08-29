from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import create_team


urlpatterns = patterns('teams',
    url(r'new/$', create_team, name='create-team'),
    url(r'created/$', TemplateView.as_view(template_name='teams/created.html'), name='team-created')
)
