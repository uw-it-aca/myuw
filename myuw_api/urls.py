from django.conf.urls import patterns, include, url
from myuw_api.views import StudClasScheCurQuarView

urlpatterns = patterns('myuw_spi.views',
                       url(r'v1/schedule/current/(?P<regid>\w{32})$',
                           StudClasScheCurQuarView().run),
                  #    url(r'v1/search/(?P<query>.*)$', SearchView().run),
)
