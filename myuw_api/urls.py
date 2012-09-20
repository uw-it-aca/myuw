from django.conf.urls import patterns, include, url
from myuw_api.views import StudClasScheCurQuar, TextbookCurQuar, InstructorContact

urlpatterns = patterns('myuw_spi.views',
                       url(r'v1/schedule/current/$', StudClasScheCurQuar().run),
                       url(r'v1/books/current/$', TextbookCurQuar().run),
                       url(r'v1/person/(?P<regid>.*)$', InstructorContact().run),
                  #    url(r'v1/search/(?P<query>.*)$', SearchView().run),
)
