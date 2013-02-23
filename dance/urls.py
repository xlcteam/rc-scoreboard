from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('dance.views',
    url(r'^$', 'index_dance', name='index'),

    url(r'^events/?$', 'events'),
    url(r'^event/(?P<event_id>\d+)/?$', 'event'),
    url(r'^event/new?$', 'new_event_dance', name='new_event_dance'),
    url(r'^results/live/?$', 'results_live'),
)
