from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('rescue.views',
    url(r'^$', 'index_rescue', name='index_rescue'),

    url(r'^competitions/?$', 'competitions'),
    url(r'^competition/(?P<competition_id>\d+)/?$', 'competition', name="competition"),
    url(r'^competition/new/?$', 'new_competition', name="new_competition"),

    url(r'^groups/?$', 'groups'),
    url(r'^group/(?P<group_id>\d+)/?$', 'group', name="group"),
    url(r'^group/new/?$', 'new_group', name="new_group"),

    url(r'^teams/?$', 'teams'),
    url(r'^team/(?P<team_id>\d+)/?$', 'team', name="team"),
    url(r'^team/new/?$', 'new_team', name='new_team'),

    url(r'^performances/generate/(?P<group_id>\d+)/?$', 'performances_generate'),
    url(r'^performances/generate/?$', 'performances_generate_listing'),

    url(r'^table/final/generate/(?P<group_id>\d+)/?$', 'table_final_generate'),
    url(r'^performance/play/(?P<performance_id>\d+)/?$', 'performance_play',
        name='performance_play'),
    url(r'^performance/save/(?P<performance_id>\d+)/?$', 'performance_save', 
        name='performance_save'),

    url(r'^results/live/?$', 'results_live'),


)
