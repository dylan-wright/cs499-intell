'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com
    
    /game/urls.py
        Django url resolvers for game app
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^games/$', views.games, name='games'),
    url(r'^games/create/$', views.create, name="create"),
    url(r'^games/(?P<pk>[0-9]+)/$', views.game_detail, name="game_detail"),
    url(r'^agents/$', views.agents, name='agents'),
    url(r'^agents/(?P<pk>[0-9]+)/$', views.agent_detail, name="agent_detail"),
    url(r'^players/$', views.players, name='players'),
    url(r'^players/(?P<pk>[0-9]+)/$', views.player_detail, name="player_detail"),
    url(r'^knowledges/$', views.knowledges, name='knowledges'),
    url(r'^knowledges/(?P<pk>[0-9]+)/$', views.knowledge_detail, name="knowledge_detail"),
    url(r'^games/submit_action/$', views.submit_action, name="submit_action"),
    url(r'^play/(?P<pk>[0-9]+)/$', views.play, name="play"),
    url(r'^games/(?P<pk>[0-9]+)/join/$', views.join, name="join")
]
