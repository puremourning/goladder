from django.conf.urls import url
from ladder import views

urlpatterns = [
    # /ladder/
    url(r'^$', views.LadderView.as_view(), name='ladder'),

    # /ladder/match/<match_id>
    url(r'^match/(?P<pk>[0-9]+)/$', 
        views.MatchView.as_view(), 
        name='match'),

    # /ladder/match/<add|amend|delete>
    url(r'^match/add/$',
        views.MatchCreate.as_view(),
        name='match-add'),
    url(r'^match/amend/(?P<pk>[0-9]+)/$',
        views.MatchAmend.as_view(),
        name='match-amend'),
    url(r'^match/delete/(?P<pk>[0-9]+)/$',
        views.MatchDelete.as_view(),
        name='match-delete'),

    # /ladder/player/<id>
    url(r'^player/(?P<pk>[0-9]+)/$', 
        views.PlayerView.as_view(), 
        name='player'),
]
