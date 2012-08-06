from django.conf.urls import patterns, include, url

urlpatterns = patterns('myuw_rws.views',
    url(r'v1/schedule/(?P<regid>\s{32})$', 
        CurQuarterClassScheView().run),
#    url(r'v1/schedule/next/(?P<regid>\s{32})$', 
#        NextQuarterClassScheView().run),
#    url(r'v1/search/(?P<query>.*)$', SearchView().run),
)
