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
from myuw.views.api.applications import Applications
from myuw.views.category import category
from myuw.views.display_dates import override
from myuw.views.message_admin import manage_messages
from myuw.views.link_admin import popular_links
from myuw.views.choose import new_site, old_site
from myuw.views.logger import log_interaction
from myuw.views.photo import show_photo
from myuw.views.academics import academics
from myuw.views.accounts import accounts
from myuw.views.profile import profile
from myuw.views.link import outbound_link
from myuw.views.api.current_schedule import StudClasScheCurQuar
from myuw.views.api.instructor_schedule import (
    InstScheCurQuar, InstScheQuar, InstSect, InstSectionDetails,
    LTIInstSectionDetails)
from myuw.views.api.finance import Finance
from myuw.views.api.hfs import HfsBalances
from myuw.views.api.future_schedule import StudClasScheFutureQuar
from myuw.views.api.prev_unfinished_schedule import (
    StudUnfinishedPrevQuarClasSche)
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
from myuw.views.search import search_res
from myuw.views.api.upass import UPass
from myuw.views.api.link import ManageLinks
from myuw.views.api.directory import MyDirectoryInfo
from myuw.views.lti.photo_list import LTIPhotoList
from myuw.views.api.visual_schedule import VisSchedCurQtr


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
    url(r'admin/messages', manage_messages, name="myuw_manage_messages"),
    url(r'admin/links/(?P<page>[0-9]+)', popular_links,
        name="myuw_popular_links_paged"),
    url(r'admin/links', popular_links, {'page': 1},
        name="myuw_popular_links"),
    url(r'^logger/(?P<interaction_type>.*)$', log_interaction
        ),
    url(r'^api/v1/academic_events$',
        AcademicEvents.as_view(),
        name="myuw_academic_calendar"),
    url(r'^api/v1/academic_events/current/$',
        AcademicEvents.as_view(), {'current': True},
        name="myuw_academic_calendar_current"),
    url(r'^api/v1/book/current/?$',
        TextbookCur.as_view(),
        name="myuw_current_book"),
    url(r'^api/v1/book/(?P<year>\d{4}),(?P<quarter>[a-z]+)'
        r'(?P<summer_term>[-,fulabterm]*)$',
        Textbook.as_view(),
        name="myuw_book_api"),
    url(r'^api/v1/categorylinks/(?P<category_id>.*?)$',
        CategoryLinks.as_view(),
        name="myuw_links_api"),
    url(r'^api/v1/deptcal/$',
        DepartmentalCalendar.as_view(),
        name="myuw_deptcal_events"),
    url(r'^api/v1/finance/$',
        Finance.as_view(),
        name="myuw_finance_api"),
    url(r'^api/v1/grad/$',
        MyGrad.as_view(),
        name="myuw_grad_api"),
    url(r'^api/v1/hfs/$',
        HfsBalances.as_view(),
        name="myuw_hfs_api"),
    url(r'^api/v1/ias/$',
        IASystem.as_view(),
        name="myuw_iasystem_api"),
    url(r'^api/v1/library/$',
        MyLibInfo.as_view(),
        name="myuw_library_api"),
    url(r'^api/v1/emaillist/(?P<year>\d{4}),'
        r'(?P<quarter>[A-Za-z]+),'
        r'(?P<curriculum_abbr>[ &%0-9A-Za-z]+),'
        r'(?P<course_number>\d{3})/'
        r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)$',
        Emaillist.as_view(),
        name="myuw_emaillist_api"),
    url(r'^api/v1/emaillist',
        Emaillist.as_view(),
        name="myuw_emaillist_api"),
    url(r'^api/v1/myplan/(?P<year>\d{4})/(?P<quarter>[a-zA-Z]+)',
        MyPlan.as_view(),
        name="myuw_myplan_api"),
    url(r'^api/v1/notices/$',
        Notices.as_view(),
        name="myuw_notices_api"),
    url(r'^api/v1/oquarters/$',
        RegisteredFutureQuarters.as_view(),
        name="myuw_other_quarters_api"),
    url(r'^api/v1/profile/$',
        MyProfile.as_view(),
        name="myuw_profile_api"),
    url(r'^api/v1/applications/',
        Applications.as_view(),
        name="myuw_applications_api"),
    url(r'api/v1/link/?$',
        ManageLinks.as_view(),
        name='myuw_manage_links'),
    url(r'^api/v1/upass/$',
        UPass.as_view(),
        name="myuw_upass_api"),
    url(r'^api/v1/schedule/current/?$',
        StudClasScheCurQuar.as_view(),
        name="myuw_current_schedule"),
    url(r'^api/v1/schedule/prev_unfinished/?$',
        StudUnfinishedPrevQuarClasSche.as_view(),
        name="myuw_prev_unfinished_schedule"),
    url(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+),'
        r'(?P<summer_term>[-,abterm]*)$',
        StudClasScheFutureQuar.as_view(),
        name="myuw_future_summer_schedule_api"),
    url(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)',
        StudClasScheFutureQuar.as_view(),
        name="myuw_future_schedule_api"),
    url(r'^api/v1/instructor_schedule/current/?$',
        InstScheCurQuar.as_view(),
        name="myuw_instructor_current_schedule_api"),
    url(r'^api/v1/instructor_schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)',
        InstScheQuar.as_view(),
        name="myuw_instructor_schedule_api"),
    url(r'^api/v1/instructor_section/(?P<section_id>.*)/?$',
        InstSect.as_view(),
        name="myuw_instructor_section_api"),
    url(r'^api/v1/instructor_section_details/(?P<section_id>.*)/?$',
        InstSectionDetails.as_view(),
        name="myuw_instructor_section_details_api"),
    url(r'^lti/api/v1/instructor_section_details/(?P<section_id>[^/]*)$',
        LTIInstSectionDetails.as_view(),
        name="myuw_lti_instructor_section_details_api"),
    url(r'^api/v1/visual_schedule/current/?$',
        VisSchedCurQtr.as_view(),
        name="myuw_current_visual_schedule"),
    url(r'^api/v1/visual_schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)',
        VisSchedCurQtr.as_view(),
        name="myuw_future_visual_schedule"),
    url(r'^api/v1/thrive/$',
        ThriveMessages.as_view(),
        name="myuw_thrive_api"),
    url(r'^api/v1/directory/$',
        MyDirectoryInfo.as_view(),
        name="myuw_directory_api"),
    url(r'^choose/new', new_site, name="myuw_pref_new_site"),
    url(r'^choose/legacy', old_site, name="myuw_pref_old_site"),
    url(r'^academics/?$', academics, name="myuw_academics_page"),
    url(r'^accounts/?$', accounts, name="myuw_accounts_page"),
    url(r'^profile/?$', profile, name="myuw_profile_page"),
    url(r'^search/?$', search_res, name="myuw_search_res_page"),
    url(r'^teaching/(?P<year>2[0-9]{3}),(?P<quarter>[A-Za-z]+),'
        r'(?P<section>[\w& ]+,\d{3}\/[A-Z][A-Z0-9]?)$',
        teaching_section, name="myuw_section_page"
        ),
    url(r'^teaching/(?P<year>2[0-9]{3}),(?P<quarter>[A-Za-z]+),'
        r'(?P<section>[\w& ]+,\d{3}\/[A-Z][A-Z0-9]?)'
        r'/students$',
        student_photo_list, name="myuw_photo_list"
        ),
    url(r'^teaching/(?P<year>2[0-9]{3}),(?P<quarter>[a-z]+)$',
        teaching, name="myuw_teaching_page"
        ),
    url(r'^teaching/?$', teaching, name="myuw_teaching_page"
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

    url(r'lti/students$',
        LTIPhotoList.as_view(), name='myuw_lti_photo_list'),
    url(r'photo/(?P<url_key>.*)', show_photo),
    url(r'out/?', outbound_link, name='myuw_outbound_link'),
    url(r'.*', index, name="myuw_home"),
]
