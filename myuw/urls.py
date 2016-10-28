from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from myuw.views.page import index, logout
from myuw.views.display_dates import override
from myuw.views.choose import new_site, old_site
from myuw.views.logger import log_interaction
from myuw.views.api.current_schedule import StudClasScheCurQuar
from myuw.views.api.finance import Finance
from myuw.views.api.hfs import HfsBalances
from myuw.views.api.future_schedule import StudClasScheFutureQuar
from myuw.views.api.grad import MyGrad
from myuw.views.api.iasystem import IASystem
from myuw.views.api.library import MyLibInfo
from myuw.views.api.profile import MyProfile
from myuw.views.api.category_links import CategoryLinks
from myuw.views.api.other_quarters import RegisteredFutureQuarters
from myuw.views.api.textbook import Textbook, TextbookCur
from myuw.views.api.notices import Notices
from myuw.views.api.myplan import MyPlan
from myuw.views.api.academic_events import AcademicEvents
from myuw.views.api.thrive import ThriveMessages
from myuw.views.page import index
from myuw.views.api.calendar import DepartmentalCalendar


urlpatterns = [
    url(r'admin/dates', override
        ),
    url(r'^logger/(?P<interaction_type>\w+)$', log_interaction
        ),
    url(r'^api/v1/academic_events$', login_required(AcademicEvents().run),
        name="myuw_academic_calendar"
        ),
    url(r'^api/v1/academic_events/current/$',
        login_required(AcademicEvents().run), {'current': True},
        name="myuw_academic_calendar_current"
        ),
    url(r'^api/v1/book/current/?$', login_required(TextbookCur().run),
        name="myuw_current_book"
        ),
    url(r'^api/v1/book/(?P<year>\d{4}),(?P<quarter>[a-z]+)'
        r'(?P<summer_term>[-,fulabterm]*)$',
        login_required(Textbook().run), name="myuw_book_api"
        ),
    url(r'^api/v1/categorylinks/(?P<category_id>.*?)$',
        login_required(CategoryLinks().run), name="myuw_links_api"
        ),
    url(r'^api/v1/deptcal/$', login_required(DepartmentalCalendar().run),
        name="myuw_deptcal_events"
        ),
    url(r'^api/v1/finance/$', login_required(Finance().run),
        name="myuw_finance_api"
        ),
    url(r'^api/v1/grad/$', login_required(MyGrad().run),
        name="myuw_grad_api"
        ),
    url(r'^api/v1/hfs/$', login_required(HfsBalances().run),
        name="myuw_hfs_api"
        ),
    url(r'^api/v1/ias/$', login_required(IASystem().run),
        name="myuw_iasystem_api"
        ),
    url(r'^api/v1/library/$', login_required(MyLibInfo().run),
        name="myuw_library_api"
        ),
    url(r'^api/v1/myplan/(?P<year>\d{4})/(?P<quarter>[a-zA-Z]+)',
        login_required(MyPlan().run),
        name="myuw_myplan_api"
        ),
    url(r'^api/v1/notices/$', login_required(Notices().run),
        name="myuw_notices_api"
        ),
    url(r'^api/v1/oquarters/$',
        login_required(RegisteredFutureQuarters().run),
        name="myuw_other_quarters_api"
        ),
    url(r'^api/v1/profile/$', login_required(MyProfile().run),
        name="myuw_profile_api"
        ),
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
    url(r'^api/v1/thrive/$', login_required(ThriveMessages().run),
        name="myuw_thrive_api"
        ),
    url(r'^choose/new', new_site, name="myuw_pref_new_site"
        ),
    url(r'^choose/legacy', old_site, name="myuw_pref_old_site"
        ),
    url(r'^logout', logout, name="myuw_logout"
        ),
    url(r'.*', index, name="myuw_home"),
]
