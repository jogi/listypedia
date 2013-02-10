from django.conf.urls import patterns, url, include
from server import views

urlpatterns = patterns('server.views',
    url(r'^$', views.index, name='index'),
)
