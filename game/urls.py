from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^games/$', views.games, name='games'),
    url(r'^games/create/$', views.create, name="create"),
    url(r'^games/(?P<pk>[0-9]+)/$', views.game_detail, name="game_detail"),
    url(r'^agents/$', views.agents, name='agents'),
    url(r'^agents/(?P<pk>[0-9]+)/$', views.agent_detail, name="agent_detail"),
]
