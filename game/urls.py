from django.conf.urls import patterns, url
from .views import view_map

urlpatterns = patterns('',
    url(r'^map/$', view_map, name='map'),
)
