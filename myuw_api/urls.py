from django.conf.urls import patterns, include, url

urlpatterns = patterns('myuw_spi.views',
                       url(r'v1/schedule/current/(?P<regid>\s{32})$', 
                           StudClasScheCurQuarView().run),
                  #    url(r'v1/search/(?P<query>.*)$', SearchView().run),
)
