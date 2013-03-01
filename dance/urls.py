from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('dance.views',
    url(r'^$', 'index_dance', name='index_dance'),

    url(r'^events/?$', 'events'),
    url(r'^event/(?P<event_id>\d+)/?$', 'event', name="event"),
    url(r'^event/new/?$', 'new_event', name='new_event'),

    url(r'^competitions/?$', 'competitions'),
    url(r'^competition/(?P<competition_id>\d+)/?$', 'competition', name="competition"),
    url(r'^competition/new/?$', 'new_competition', name="new_competition"),

    url(r'^groups/?$', 'groups'),
    url(r'^group/(?P<group_id>\d+)/?$', 'group', name="group"),
    url(r'^group/new/?$', 'new_group', name='new_group'),

    url(r'^teams/?$', 'teams'),
    url(r'^team/(?P<team_id>\d+)/?$', 'team', name="team"),
    url(r'^team/new/?$', 'new_team', name='new_team'),

    url(r'^results/live/?$', 'results_live'),
)
