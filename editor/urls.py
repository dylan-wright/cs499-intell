from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^edit/$', views.edit, name='edit'),

    url(r'^edit/character/$', views.CharacterList.as_view(), name="character-view"),
    url(r'^edit/character/add/$', views.CharacterCreate.as_view(), name="character-add"),
    url(r'^edit/character/(?P<pk>[0-9]+)/$', views.CharacterUpdate.as_view(), name="character-update"),
    url(r'^edit/character/(?P<pk>[0-9]+)/delete/$', views.CharacterDelete.as_view(), name="character-delete")
]
