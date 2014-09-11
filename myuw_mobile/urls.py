from django.conf.urls import patterns, include, url
from myuw_mobile.views.mobile_login import user_login
from myuw_mobile.views.api.contact import InstructorContact
from myuw_mobile.views.api.current_schedule import StudClasScheCurQuar
from myuw_mobile.views.api.finance import Finance
from myuw_mobile.views.api.grades import Grades
from myuw_mobile.views.api.hfs import HfsBalances
from myuw_mobile.views.api.future_schedule import StudClasScheFutureQuar
from myuw_mobile.views.api.library import MyLibInfo
from myuw_mobile.views.api.links import QuickLinks
from myuw_mobile.views.api.category_links import CategoryLinks
from myuw_mobile.views.api.other_quarters import RegisteredFutureQuarters
from myuw_mobile.views.api.uwemail import UwEmail
from myuw_mobile.views.api.textbook import Textbook
from myuw_mobile.views.api.weekly import Weekly
from myuw_mobile.views.logout import Logout
from myuw_mobile.views.api.notices import Notices
from myuw_mobile.views.page import index

urlpatterns = patterns('myuw_mobile.views',
    url(r'login', 'mobile_login.user_login'),
    url(r'test', 'test.index'),
    url(r'^link/(?P<linkid>\d+)$', 'link.show_link'),
    url(r'^logger/(?P<interaction_type>\w+)$', 'logger.log_interaction'),
    url(r'logout', Logout.as_view()),
    url(r'^api/v1/book/(current|(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*))$',
       Textbook().run),
    url(r'^api/v1/schedule/current/?$', StudClasScheCurQuar().run),
    url(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$',
        StudClasScheFutureQuar().run),
    url(r'^api/v1/links/$', QuickLinks().run),
    url(r'^api/v1/categorylinks/(?P<category_id>.*?)$', CategoryLinks().run),
    url(r'^api/v1/person/(?P<regid>[0-9A-F]{32})$', InstructorContact().run),
    url(r'^api/v1/finance/$', Finance().run),                   
    url(r'^api/v1/hfs/$', HfsBalances().run),
    url(r'^api/v1/library/$', MyLibInfo().run),
    url(r'^api/v1/oquarters/$', RegisteredFutureQuarters().run),
    url(r'^api/v1/grades/$', Grades().run),
    url(r'^api/v1/notices/$', Notices().run),
    url(r'^api/v1/uwemail/$', UwEmail().run),
    url(r'^api/v1/current_week/$', Weekly().run),
    url(r'^api/v1/grades/(?P<year>[0-9]{4}),(?P<quarter>[a-z]+)$', Grades().run),
    url(r'.*', 'page.index'),
)
