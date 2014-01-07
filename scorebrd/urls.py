from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.conf import settings

handler404 = 'scorebrd.views.error_404'

urlpatterns = patterns('scorebrd.views',
    url(r'^$', 'index', name='main_index'),
    url(r'^login', 'my_login', name='login'),
    url(r'^logout', 'my_logout', name='logout'),
)

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^staticed/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
