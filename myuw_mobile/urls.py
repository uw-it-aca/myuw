from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('myuw_mobile.views',
    url(r'^my/$', 'index'),
#    url(r'^my/menu/$', 'menu'),
#    url(r'^my/week/$', 'week'),
)
