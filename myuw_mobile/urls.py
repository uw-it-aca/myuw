from django.conf.urls import patterns, include, url
from myuw_mobile.views.mobile_login import user_login
from myuw_mobile.views.api.contact import InstructorContact
from myuw_mobile.views.api.current_schedule import StudClasScheCurQuar
from myuw_mobile.views.api.finance import Finance
from myuw_mobile.views.api.grades import Grades
from myuw_mobile.views.api.hfs import HfsBalances
from myuw_mobile.views.api.future_schedule import StudClasScheFutureQuar
from myuw_mobile.views.api.library import MyLibInfo
from myuw_mobile.views.api.category_links import CategoryLinks
from myuw_mobile.views.api.other_quarters import RegisteredFutureQuarters
from myuw_mobile.views.api.uwemail import UwEmail
from myuw_mobile.views.api.textbook import Textbook
from myuw_mobile.views.api.weekly import Weekly
from myuw_mobile.views.api.term import Term
from myuw_mobile.views.logout import Logout
from myuw_mobile.views.api.notices import Notices
from myuw_mobile.views.page import index
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('myuw_mobile.views',
    url(r'login', 'mobile_login.user_login'),
    url(r'test', 'test.index'),
    url(r'^logger/(?P<interaction_type>\w+)$', 'logger.log_interaction'),
    url(r'logout', login_required(Logout.as_view())),
    url(r'^api/v1/book/(current|(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*))$',
       login_required(Textbook().run)),
    url(r'^api/v1/schedule/current/?$', login_required(StudClasScheCurQuar().run)),
    url(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$',
        login_required(StudClasScheFutureQuar().run)),
    url(r'^api/v1/categorylinks/(?P<category_id>.*?)$', login_required(CategoryLinks().run)),
    url(r'^api/v1/person/(?P<regid>[0-9A-F]{32})$', login_required(InstructorContact().run)),
    url(r'^api/v1/finance/$', login_required(Finance().run)),
    url(r'^api/v1/hfs/$', login_required(HfsBalances().run)),
    url(r'^api/v1/library/$', login_required(MyLibInfo().run)),
    url(r'^api/v1/oquarters/$', login_required(RegisteredFutureQuarters().run)),
    url(r'^api/v1/grades/$', login_required(Grades().run)),
    url(r'^api/v1/notices/$', login_required(Notices().run)),
    url(r'^api/v1/uwemail/$', login_required(UwEmail().run)),
    url(r'^api/v1/current_week/$', login_required(Weekly().run)),
    url(r'^api/v1/term/current/$', login_required(Term().run)),
    url(r'^api/v1/grades/(?P<year>[0-9]{4}),(?P<quarter>[a-z]+)$', login_required(Grades().run)),
    url(r'.*', 'page.index'),
)
