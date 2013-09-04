from django.conf.urls import patterns, url
from .views import (view_map,
                    view_stage,
                    download_description,
                    download_test_file,
                    submit_stage,
                    leaderboard)


urlpatterns = patterns('',
    url(r'^$', view_map, name='game'),
    url(r'^leaderboard/$', leaderboard, name='leaderboard'),
    url(r'^stage/(?P<stage_id>[0-9]+)/$', view_stage, name='view-stage'),
    url(r'^stage/(?P<stage_id>[0-9]+)/description/(?P<lang>(en|gr))/$', download_description, name='download-description'),
    url(r'^stage/(?P<stage_id>[0-9]+)/download/$', download_test_file, name='download-test-file'),
    url(r'^stage/(?P<stage_id>[0-9]+)/submit/$', submit_stage, name='submit-stage')
)
