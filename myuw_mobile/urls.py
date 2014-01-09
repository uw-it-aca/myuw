from django.conf.urls import patterns, include, url
from myuw_mobile.views.page import index
from myuw_mobile.views.mobile_login import user_login
from myuw_mobile.views.api.schedule_api import StudClasScheCurQuar, StudClasScheFutureQuar
from myuw_mobile.views.api.contact_api import InstructorContact
from myuw_mobile.views.api.textbook_api import TextbookCurQuar
from myuw_mobile.views.api.links_api import QuickLinks
from myuw_mobile.views.api.stud_finances_api import AccountBalances
from myuw_mobile.views.api.other_quarters_api import RegisteredFutureQuarters
from myuw_mobile.views.api.grades import Grades
from myuw_mobile.views.logout import Logout

urlpatterns = patterns('myuw_mobile.views',
    url(r'login', 'mobile_login.user_login'),
    url(r'^link/(?P<linkid>\d+)$', 'link.show_link'),
    url(r'^logger/(?P<interaction_type>\w+)$', 'logger.log_interaction'),
    url(r'logout', Logout.as_view()),
    url(r'^api/v1/books/current/$', TextbookCurQuar().run),
#    url(r'^api/v1/book/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$',
#        TextbookFutureQuar().run),
    url(r'^api/v1/schedule/current/?$', StudClasScheCurQuar().run),
    url(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$',
        StudClasScheFutureQuar().run),
    url(r'^api/v1/links/$', QuickLinks().run),
    url(r'^api/v1/person/(?P<regid>[0-9A-F]{32})$', InstructorContact().run),
    url(r'^api/v1/finabala/$', AccountBalances().run),
    url(r'^api/v1/oquarters/$', RegisteredFutureQuarters().run),
    url(r'^api/v1/grades/$', Grades().run),
    url(r'^api/v1/grades/(?P<year>[0-9]{4}),(?P<quarter>[a-z]+)$', Grades().run),
    url(r'.*', 'page.index'),
)
