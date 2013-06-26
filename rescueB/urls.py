from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('rescueB.views',
  url(r'^$', 'index_rescueB', name='index_rescueB'),
  url(r'^map/new$', 'mapeditor_view'),
  url(r'^map/save', 'mapeditor_save'),
  url(r'^map/edit/(?P<map_id>\d+)', 'mapeditor_edit'),
  url(r'^map/listing', 'mapeditor_listing'),
)
