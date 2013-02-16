from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('scorebrd.views',
    url(r'^$', 'index', name='index'),
    url(r'^login/', 'my_login', name='login'),
    url(r'^logout/', 'my_logout', name='logout'),
)
