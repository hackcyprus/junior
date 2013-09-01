
from django.conf.urls import patterns, url
from .views import view_map, view_stage, download_test_file

urlpatterns = patterns('',
    url(r'^map/$', view_map, name='map'),
    url(r'^stage/(?P<stage_id>\d)$', view_stage, name='view-stage'),
    url(r'^stage/(?P<stage_id>\d)/download/$', download_test_file, name='download-test-file')
)
