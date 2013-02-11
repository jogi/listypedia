from django.conf.urls import patterns, url, include
from server import views
import os
site_media = os.path.join(os.path.dirname(__file__), '../site_media')
urlpatterns = patterns('server.views',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': site_media, 'show_indexes' : False}),
    url(r'list/create/', 'create_list', name='create_list'),
    url(r'signup/', 'signup', name='signup'),
    url(r'^$', views.index, name='index'),
)
