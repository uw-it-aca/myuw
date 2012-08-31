from django.conf.urls import patterns, include, url
from myuw_mobile.views import index

urlpatterns = patterns('myuw_mobile.views',
    url(r'^(?!api)', 'index'),
#    url(r'^menu/$', 'menu'),
#    url(r'^week/$', 'week'),
)
