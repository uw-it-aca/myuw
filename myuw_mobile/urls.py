from django.conf.urls import patterns, include, url
from myuw_mobile.views.page import index, myuw_login
from myuw_mobile.views.api import StudClasScheCurQuar, TextbookCurQuar, InstructorContact

urlpatterns = patterns('myuw_mobile.views.page',
    url(r'login', 'myuw_login'),
    url(r'support', 'support'),
    url(r'^visual', 'index'),
    url(r'^textbooks', 'index'),
    url(r'^instructor', 'index'),
    url(r'^links', 'index'),
    url(r'^$', 'index'),
)

urlpatterns += patterns('myuw_mobile.views.api',
                       url(r'v1/schedule/current/$', StudClasScheCurQuar().run),
                       url(r'v1/books/current/$', TextbookCurQuar().run),
                       url(r'v1/person/(?P<regid>.*)$', InstructorContact().run),
                  #    url(r'v1/search/(?P<query>.*)$', SearchView().run),
)
