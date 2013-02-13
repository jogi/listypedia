import os

from django.conf.urls import patterns, url, include

from server import views


site_media = os.path.join(os.path.dirname(__file__), '../site_media')


urlpatterns = patterns('server.views',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media, 'show_indexes': False}),
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^signup/', 'signup', name='signup'),
    url(r'^search/', 'search', name='search'),
    url(r'^login/', 'login', name='login'),
    url(r'^logout/', 'logout', name='logout'),
    url(r'^list/create/', 'create_list', name='create_list'),
    url(r'^list/follow/', 'add_follower', name='add_follower'),
    url(r'^list/(?P<slug>[a-zA-Z0-9_.-]+)/$', 'view_list', name='view_list'),
    url(r'^list/(?P<slug>[a-zA-Z0-9_.-]+)/item/add/', 'add_item', name='add_item'),
)
