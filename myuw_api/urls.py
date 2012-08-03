from django.conf.urls import patterns, include, url

urlpatterns = patterns('myuw_rws.views',
    url(r'v1/schedule/(?P<year>\d{4})/(?P<quarter_code>\d{1})/(?P<regid>\s{32})$', 
        ClassScheView().run),
    url(r'v1/search/(?P<query>.*)$', SearchView().run),
)
