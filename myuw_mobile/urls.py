from django.conf.urls import patterns, include, url
from myuw_mobile.views.mobile_login import user_login
from myuw_mobile.views.api.current_schedule import StudClasScheCurQuar
from myuw_mobile.views.api.finance import Finance
from myuw_mobile.views.api.hfs import HfsBalances
from myuw_mobile.views.api.future_schedule import StudClasScheFutureQuar
from myuw_mobile.views.api.library import MyLibInfo
from myuw_mobile.views.api.profile import MyProfile
from myuw_mobile.views.api.category_links import CategoryLinks
from myuw_mobile.views.api.other_quarters import RegisteredFutureQuarters
from myuw_mobile.views.api.uwemail import UwEmail
from myuw_mobile.views.api.textbook import Textbook
from myuw_mobile.views.logout import Logout
from myuw_mobile.views.api.notices import Notices
from myuw_mobile.views.api.academic_events import AcademicEvents
from myuw_mobile.views.page import index
from django.contrib.auth.decorators import login_required


urlpatterns = patterns(
    'myuw_mobile.views',
    url(r'login', 'mobile_login.user_login'),
    url(r'admin/dates', 'display_dates.override'),
    url(r'^logger/(?P<interaction_type>\w+)$', 'logger.log_interaction'),
    url(r'logout', login_required(Logout.as_view())),
    url(r'^api/v1/book/(?P<year>\d{4}),(?P<quarter>[a-z]+)'
        r'(?P<summer_term>[-,abterm]*)$',
        login_required(Textbook().run),
        name="myuw_book_api"
        ),

    url(r'^api/v1/categorylinks/(?P<category_id>.*?)$',
        login_required(CategoryLinks().run),
        name="myuw_links_api"),
    url(r'^api/v1/finance/$', login_required(Finance().run),
        name="myuw_finance_api"),
    url(r'^api/v1/hfs/$', login_required(HfsBalances().run),
        name="myuw_hfs_api"),
    url(r'^api/v1/library/$', login_required(MyLibInfo().run),
        name="myuw_library_api"),
    url(r'^api/v1/oquarters/$',
        login_required(RegisteredFutureQuarters().run),
        name="myuw_other_quarters_api"
        ),
    url(r'^api/v1/profile/$', login_required(MyProfile().run),
        name="myuw_profile_api"),
    url(r'^api/v1/notices/$', login_required(Notices().run),
        name="myuw_notices_api"),
    url(r'^api/v1/uwemail/$', login_required(UwEmail().run),
        name="myuw_email_api"),
    url(r'^api/v1/schedule/current/?$',
        login_required(StudClasScheCurQuar().run),
        name="myuw_current_schedule"
        ),
    url(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+),'
        r'(?P<summer_term>[-,abterm]*)$',
        login_required(StudClasScheFutureQuar().run),
        name="myuw_future_summer_schedule_api"
        ),
    url(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)',
        login_required(StudClasScheFutureQuar().run),
        name="myuw_future_schedule_api"
        ),
    url(r'^api/v1/academic_events$', login_required(AcademicEvents().run)),
    url(r'^api/v1/academic_events/current$',
        login_required(AcademicEvents().run), {'current': True}),
    url(r'.*', 'page.index', name="myuw_home"),
)
