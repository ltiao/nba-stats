from django.conf.urls import patterns, url
from nba.views import PlayerList

urlpatterns = patterns('',
    url(r'^players/$', PlayerList.as_view()),
)
