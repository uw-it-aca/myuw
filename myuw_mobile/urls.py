from django.conf.urls import patterns, include, url
from myuw_mobile.views.page import index, myuw_login
from myuw_mobile.views.schedule_api import StudClasScheCurQuar
from myuw_mobile.views.contact_api import InstructorContact
from myuw_mobile.views.textbook_api import TextbookCurQuar

urlpatterns = patterns('myuw_mobile.views.page',
    url(r'login', 'myuw_login'),
    url(r'support', 'support'),
    url(r'^visual', 'index'),
    url(r'^textbooks', 'index'),
    url(r'^instructor', 'index'),
    url(r'^links', 'index'),
    url(r'^$', 'index'),
    url(r'^api/v1/books/current/$', TextbookCurQuar().run),
    url(r'^api/v1/schedule/current/$', StudClasScheCurQuar().run),
    url(r'^api/v1/person/(?P<regid>.*)$', InstructorContact().run),
)
