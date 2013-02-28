from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

handler404 = 'scorebrd.views.404_error'

urlpatterns = patterns('scorebrd.views',
    url(r'^$', 'index', name='main_index'),
    url(r'^login', 'my_login', name='login'),
    url(r'^logout', 'my_logout', name='logout'),
)
