from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('dance.views',
    url(r'^$', 'index_dance', name='index'),
)
