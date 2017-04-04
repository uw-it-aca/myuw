from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from myuw.views.page import logout
from myuw.views.index import index
from myuw.views.teaching import teaching, teaching_section, student_photo_list
from myuw.views.notices import notices
from myuw.views.thrive import thrive
from myuw.views.thrive_messages import thrive_messages
from myuw.views.academic_calendar import academic_calendar
from myuw.views.future_quarters import future_quarters
from myuw.views.textbooks import textbooks
from myuw.views.category import category
from myuw.views.display_dates import override
from myuw.views.choose import new_site, old_site
from myuw.views.logger import log_interaction
from myuw.views.photo import show_photo
from myuw.views.accounts import accounts
from myuw.views.api.current_schedule import StudClasScheCurQuar
from myuw.views.api.instructor_schedule import (InstScheCurQuar, InstScheQuar,
                                                InstSect, InstSectionDetails)
from myuw.views.api.finance import Finance
from myuw.views.api.hfs import HfsBalances
from myuw.views.api.future_schedule import StudClasScheFutureQuar
from myuw.views.api.grad import MyGrad
from myuw.views.api.iasystem import IASystem
from myuw.views.api.library import MyLibInfo
from myuw.views.api.emaillist import Emaillist
from myuw.views.api.profile import MyProfile
from myuw.views.api.category_links import CategoryLinks
from myuw.views.api.other_quarters import RegisteredFutureQuarters
from myuw.views.api.textbook import Textbook, TextbookCur
from myuw.views.api.notices import Notices
from myuw.views.api.myplan import MyPlan
from myuw.views.api.academic_events import AcademicEvents
from myuw.views.api.thrive import ThriveMessages
from myuw.views.api.calendar import DepartmentalCalendar

urlpatterns = []

# debug routes error pages
if settings.DEBUG:
    from django.views.defaults import server_error, page_not_found
    urlpatterns += [
        url(r'^500/?$', server_error),
        url(r'^404/?$', login_required(page_not_found),
            kwargs={'exception': Exception("Page not Found")}),
    ]

urlpatterns += [
    url(r'admin/dates', override, name="myuw_date_override"
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
    url(r'^api/v1/emaillist/(?P<year>\d{4}),'
        r'(?P<quarter>[A-Za-z]+),'
        r'(?P<curriculum_abbr>[&%0-9A-Za-z]+),'
        r'(?P<course_number>\d{3})/'
        r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)$',
        login_required(Emaillist().run),
        name="myuw_emaillist_api"
        ),
    url(r'^api/v1/emaillist',
        login_required(Emaillist().run),
        name="myuw_emaillist_api"
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
    url(r'^api/v1/instructor_schedule/current/?$',
        login_required(InstScheCurQuar().run),
        name="myuw_instructor_current_schedule_api"
        ),
    url(r'^api/v1/instructor_schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)',
        login_required(InstScheQuar().run),
        name="myuw_instructor_schedule_api"
        ),
    url(r'^api/v1/instructor_section/(?P<year>\d{4}),(?P<quarter>[a-zA-Z]+),'
        r'(?P<curriculum>[\w& ]+),(?P<course_number>\d{3})\/'
        r'(?P<course_section>[A-Z][A-Z0-9]?)$',
        login_required(InstSect().run),
        name="myuw_instructor_section_api"
        ),
    url(r'^api/v1/instructor_section_details/(?P<year>\d{4}),'
        r'(?P<quarter>[a-zA-Z]+),'
        r'(?P<curriculum>[\w& ]+),(?P<course_number>\d{3})\/'
        r'(?P<course_section>[A-Z][A-Z0-9]?)$',
        login_required(InstSectionDetails().run),
        name="myuw_instructor_section_details_api"
        ),
    url(r'^api/v1/thrive/$', login_required(ThriveMessages().run),
        name="myuw_thrive_api"
        ),
    url(r'^choose/new', new_site, name="myuw_pref_new_site"
        ),
    url(r'^choose/legacy', old_site, name="myuw_pref_old_site"
        ),
    url(r'accounts/?$', accounts, name="myuw_accounts_page"),
    url(r'^teaching/?$', teaching, name="myuw_teaching_page"
        ),
    url(r'^teaching/'
        r'(?P<section>\d{4},[a-zA-Z]+,[\w& ]+,\d{3}\/[A-Z][A-Z0-9]?)$',
        teaching_section, name="myuw_section_page"
        ),
    url(r'^teaching/(?P<section>\d{4},[a-zA-Z]+,[\w& ]+,\d{3}\/[A-Z][A-Z0-9]?)'
        r'/students$',
        student_photo_list, name="myuw_photo_list"
        ),

    url(r'^notices/?', notices, name="myuw_notices_page"
        ),
    url(r'^thrive_messages/?', thrive_messages,
        name="myuw_thrive_messages_page"),
    url(r'^thrive/?', thrive, name="myuw_thrive_page"
        ),
    url(r'^academic_calendar/?', academic_calendar,
        name="myuw_academic_calendar_page"),
    url(r'^future_quarters/(?P<quarter>2[0-9]{3},[-,a-z]+)',
        future_quarters, name="myuw_future_quarters_page"),
    url(r'^textbooks/(?P<term>2[0-9]{3},[-,a-z]+)/(?P<textbook>[%A-Z0-9]+)',
        textbooks, name="myuw_textbooks_page"),
    url(r'^textbooks/(?P<term>2[0-9]{3},[-,a-z]+)',
        textbooks, name="myuw_textbooks_page"),
    url(r'^textbooks/?',
        textbooks, name="myuw_textbooks_page"),
    url(r'^resource(/((?P<category>[a-z]+)?(/(?P<topic>[a-z]+))?)?)?',
        category, name="myuw_resource_page"),
    url(r'^logout', logout, name="myuw_logout"
        ),

    url(r'photo/(?P<url_key>.*)', show_photo),
    url(r'.*', index, name="myuw_home"),
]
