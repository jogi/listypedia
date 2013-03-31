import os

from django.conf.urls import patterns, url


site_media = os.path.join(os.path.dirname(__file__), '../site_media')


urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media, 'show_indexes': False}),
    url(r'^$', 'server.views.index', name='index'),
    url(r'^home/', 'server.views.home', name='home'),
    url(r'^signup/', 'server.views.signup', name='signup'),
    url(r'^search/', 'server.views.search', name='search'),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^list/create/', 'server.views.create_list', name='create_list'),
    url(r'^list/(?P<slug>[a-zA-Z0-9_.-]+)/follow/', 'server.views.add_follower', name='add_follower'),
    url(r'^list/(?P<slug>[a-zA-Z0-9_.-]+)/unfollow/', 'server.views.remove_follower', name='remove_follower'),
    url(r'^list/(?P<slug>[a-zA-Z0-9_.-]+)/$', 'server.views.view_list', name='view_list'),
    url(r'^list/(?P<slug>[a-zA-Z0-9_.-]+)/invite/', 'server.views.invite_collaborator', name='invite_collaborator'),
    url(r'^list/(?P<slug>[a-zA-Z0-9_.-]+)/item/add/', 'server.views.add_item', name='add_item'),
    url(r'^item/(?P<item_id>[0-9]+)/delete/', 'server.views.delete_item', name='delete_item'),
    url(r'^list/invitation/accept/', 'server.views.accept_invitation', name='accept_invitation'),
    url(r'^pageinfo/', 'server.views.page_info', name='page_info'),
    url(r'^b/lists/', 'server.views.user_lists', name='user_lists'),
)
