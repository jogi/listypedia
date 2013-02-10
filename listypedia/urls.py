import os
from django.conf.urls import patterns, include, url

site_media = os.path.join(os.path.dirname(__file__), '../site_media')

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'listypedia.views.home', name='home'),
    # url(r'^listypedia/', include('listypedia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': site_media, 'show_indexes' : False}),
    url(r'^', include('server.urls')),
)
