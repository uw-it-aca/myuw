from django.conf.urls import patterns, include, url

urlpatterns = patterns('myuw_mobile.views',
    url(r'^$', 'index'),
#    url(r'^menu/$', 'menu'),
#    url(r'^week/$', 'week'),
)
