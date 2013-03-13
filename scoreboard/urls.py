from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   #url(r'^$', include('scorebrd.views.index'), name='index')
   #url(r'^login/', include('scorebrd.views.my_login'), name='login'),
   #url(r'^logout/', include('scorebrd.views.my_logout', name='logout')),

    url(r'^dance/', include('dance.urls')),
    url(r'^soccer/', include('soccer.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('django_socketio.urls')),
    url(r'', include('scorebrd.urls')),


)
