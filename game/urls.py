
from django.conf.urls import patterns, url
from .views import view_map, view_stage, download_test_file, submit_stage

urlpatterns = patterns('',
    url(r'^map/$', view_map, name='map'),
    url(r'^stage/(?P<stage_id>[0-9]+)/$', view_stage, name='view-stage'),
    url(r'^stage/(?P<stage_id>[0-9]+)/download/$', download_test_file, name='download-test-file'),
    url(r'^stage/(?P<stage_id>[0-9]+)/submit/$', submit_stage, name='submit-stage')
)
