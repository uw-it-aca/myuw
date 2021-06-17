# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import re_path
from django.contrib.auth.decorators import login_required
from myuw.views.page import logout
from myuw.views.home import home
from myuw.views.teaching import teaching, teaching_section, student_photo_list
from myuw.views.notices import notices
from myuw.views.thrive import thrive
from myuw.views.thrive_messages import thrive_messages
from myuw.views.academic_calendar import academic_calendar
from myuw.views.future_quarters import future_quarters
from myuw.views.textbooks import textbooks
from myuw.views.category import category
from myuw.views.display_dates import override
from myuw.views.message_admin import manage_messages
from myuw.views.link_admin import popular_links
from myuw.views.logger import log_interaction
from myuw.views.photo import show_photo
from myuw.views.academics import academics
from myuw.views.accounts import accounts
from myuw.views.profile import profile
from myuw.views.husky_experience import husky_experience
from myuw.views.link import outbound_link
from myuw.views.resources import resources
from myuw.views.api.adviser import Advisers
from myuw.views.rest_search import MyUWRestSearchView
from myuw.views.api.affiliation import Affiliation
from myuw.views.api.applications import Applications
from myuw.views.api.banner_message import CloseBannerMsg, TurnOffPopup
from myuw.views.api.current_schedule import StudClasScheCurQuar
from myuw.views.api.instructor_section import (InstSectionDetails,
                                               LTIInstSectionDetails)
from myuw.views.api.instructor_schedule import (InstScheCurQuar, InstScheQuar,
                                                InstSect)
from myuw.views.api.instructor_section_display import \
    CloseMinicard, PinMinicard
from myuw.views.api.finance import Finance
from myuw.views.api.hfs import HfsBalances
from myuw.views.api.future_schedule import StudClasScheFutureQuar
from myuw.views.api.prev_unfinished_schedule import \
    StudUnfinishedPrevQuarClasSche
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
from myuw.views.api.visual_schedule import VisSchedCurQtr, VisSchedOthrQtr
from myuw.views.api.hx_toolkit import HxToolkitMessage, HxToolkitWeekMessage, \
    HxToolkitMessageList
from myuw.views.api.resources import (ResourcesList,
                                      ResourcesPin,
                                      PinnedResources)
from myuw.views.notice_admin import create_notice, edit_notice, list_notices


urlpatterns = []


# debug routes error pages
if settings.DEBUG:
    from django.views.defaults import server_error, page_not_found
    urlpatterns += [
        re_path(r'^500/?$', server_error),
        re_path(r'^404/?$', login_required(page_not_found),
                kwargs={'exception': Exception("Page not Found")}),
    ]

urlpatterns += [
    re_path(r'admin/dates', override, name="myuw_date_override"),
    re_path(r'admin/messages', manage_messages, name="myuw_manage_messages"),
    re_path(r'admin/notices/(?P<notice_id>[0-9]+)', edit_notice,
            name="myuw_edit_notices"),
    re_path(r'admin/notice_create', create_notice, name="myuw_create_notice"),
    re_path(r'admin/notices', list_notices, name="myuw_manage_notices"),
    re_path(r'admin/links/(?P<page>[0-9]+)', popular_links,
            name="myuw_popular_links_paged"),
    re_path(r'admin/links', popular_links, {'page': 1},
            name="myuw_popular_links"),
    re_path(r'^logger/(?P<interaction_type>.*)$', log_interaction),
    re_path(r'^restsearch/(\w+)/(.*)$',
            MyUWRestSearchView.as_view(), name="myuw_rest_search"),
    re_path(r'api/v1/close_banner_message',
            CloseBannerMsg.as_view(),
            name="myuw_close_banner_message"),
    re_path(r'api/v1/turn_off_tour_popup',
            TurnOffPopup.as_view(),
            name="myuw_turn_off_tour_popup"),
    re_path(r'^api/v1/academic_events/$',
            AcademicEvents.as_view(),
            name="myuw_academic_calendar"),
    re_path(r'^api/v1/academic_events/current/$',
            AcademicEvents.as_view(), {'current': True},
            name="myuw_academic_calendar_current"),
    re_path(r'^api/v1/advisers/?$',
            Advisers.as_view(),
            name="myuw_advisers_api"),
    re_path(r'^api/v1/affiliation/?$',
            Affiliation.as_view(),
            name="myuw_affiliation"),
    re_path(r'^api/v1/book/current/?$',
            TextbookCur.as_view(),
            name="myuw_current_book"),
    re_path(r'^api/v1/book/(?P<year>\d{4}),(?P<quarter>[a-z]+)'
            r'(?P<summer_term>[-,fulabterm]*)$',
            Textbook.as_view(),
            name="myuw_book_api"),
    re_path(r'^api/v1/categorylinks/(?P<category_id>.*?)$',
            CategoryLinks.as_view(),
            name="myuw_links_api"),
    re_path(r'^api/v1/deptcal/$',
            DepartmentalCalendar.as_view(),
            name="myuw_deptcal_events"),
    re_path(r'^api/v1/finance/$',
            Finance.as_view(),
            name="myuw_finance_api"),
    re_path(r'^api/v1/grad/$',
            MyGrad.as_view(),
            name="myuw_grad_api"),
    re_path(r'^api/v1/hfs/$',
            HfsBalances.as_view(),
            name="myuw_hfs_api"),
    re_path(r'^api/v1/ias/$',
            IASystem.as_view(),
            name="myuw_iasystem_api"),
    re_path(r'^api/v1/library/$',
            MyLibInfo.as_view(),
            name="myuw_library_api"),
    re_path(r'^api/v1/emaillist/(?P<year>\d{4}),'
            r'(?P<quarter>[A-Za-z]+),'
            r'(?P<curriculum_abbr>[ &%0-9A-Za-z]+),'
            r'(?P<course_number>\d{3})/'
            r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)$',
            Emaillist.as_view(),
            name="myuw_emaillist_api"),
    re_path(r'^api/v1/emaillist',
            Emaillist.as_view(),
            name="myuw_emaillist_api"),
    re_path(r'^api/v1/myplan/(?P<year>\d{4})/(?P<quarter>[a-zA-Z]+)',
            MyPlan.as_view(),
            name="myuw_myplan_api"),
    re_path(r'^api/v1/notices/$',
            Notices.as_view(),
            name="myuw_notices_api"),
    re_path(r'^api/v1/oquarters/$',
            RegisteredFutureQuarters.as_view(),
            name="myuw_other_quarters_api"),
    re_path(r'^api/v1/profile/$',
            MyProfile.as_view(),
            name="myuw_profile_api"),
    re_path(r'^api/v1/applications/',
            Applications.as_view(),
            name="myuw_applications_api"),
    re_path(r'api/v1/link/?$',
            ManageLinks.as_view(),
            name='myuw_manage_links'),
    re_path(r'^api/v1/upass/$',
            UPass.as_view(),
            name="myuw_upass_api"),
    re_path(r'^api/v1/schedule/current/?$',
            StudClasScheCurQuar.as_view(),
            name="myuw_current_schedule"),
    re_path(r'^api/v1/schedule/prev_unfinished/?$',
            StudUnfinishedPrevQuarClasSche.as_view(),
            name="myuw_prev_unfinished_schedule"),
    re_path(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+),'
            r'(?P<summer_term>[-,abterm]*)$',
            StudClasScheFutureQuar.as_view(),
            name="myuw_future_summer_schedule_api"),
    re_path(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)',
            StudClasScheFutureQuar.as_view(),
            name="myuw_future_schedule_api"),
    re_path(r'^api/v1/instructor_schedule/current/?$',
            InstScheCurQuar.as_view(),
            name="myuw_instructor_current_schedule_api"),
    re_path(r'^api/v1/instructor_schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)',
            InstScheQuar.as_view(),
            name="myuw_instructor_schedule_api"),
    re_path(r'^api/v1/instructor_section/(?P<section_id>.*)/?$',
            InstSect.as_view(),
            name="myuw_instructor_section_api"),
    re_path(r'^api/v1/instructor_section_details/(?P<section_id>.*)/?$',
            InstSectionDetails.as_view(),
            name="myuw_instructor_section_details_api"),
    re_path(r'^lti/api/v1/instructor_section_details/(?P<section_id>[^/]*)$',
            LTIInstSectionDetails.as_view(),
            name="myuw_lti_instructor_section_details_api"),
    re_path(r'api/v1/inst_section_display/(?P<section_label>.*)/close_mini',
            CloseMinicard.as_view(),
            name="myuw_inst_section_display_close_mini"),
    re_path(r'api/v1/inst_section_display/(?P<section_label>.*)/pin_mini',
            PinMinicard.as_view(),
            name="myuw_inst_section_display_pin_mini"),
    re_path(r'^api/v1/visual_schedule/current/?$',
            VisSchedCurQtr.as_view(),
            name="myuw_current_visual_schedule"),
    re_path(r'^api/v1/visual_schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+),'
            r'(?P<summer_term>[-,abterm]*)$',
            VisSchedOthrQtr.as_view(),
            name="myuw_future_summer_visual_schedule"),
    re_path(r'^api/v1/visual_schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)',
            VisSchedOthrQtr.as_view(),
            name="myuw_future_visual_schedule"),
    re_path(r'^api/v1/thrive/$',
            ThriveMessages.as_view(),
            name="myuw_thrive_api"),
    re_path(r'^api/v1/hx_toolkit/week/$',
            HxToolkitWeekMessage.as_view(),
            name="myuw_hxtoolkit_week_api"),
    re_path(r'^api/v1/hx_toolkit/list/$',
            HxToolkitMessageList.as_view(),
            name="myuw_hxtoolkit_list_api"),
    re_path(r'^api/v1/hx_toolkit/(?P<article_id>.*?)$',
            HxToolkitMessage.as_view(),
            name="myuw_hxtoolkit_api"),
    re_path(r'^api/v1/directory/$',
            MyDirectoryInfo.as_view(),
            name="myuw_directory_api"),
    re_path(r'^api/v1/resources/$',
            ResourcesList.as_view(),
            name="myuw_resources_api"),
    re_path(r'^api/v1/resources/(?P<category_id>.*?)/pin$',
            ResourcesPin.as_view(),
            name="myuw_resources_pin_api"),
    re_path(r'^api/v1/resources/pinned/$',
            PinnedResources.as_view(),
            name="myuw_resources_pinned_api"),
    re_path(r'^academics/?$', academics, name="myuw_academics_page"),
    re_path(r'^accounts/?$', accounts, name="myuw_accounts_page"),
    re_path(r'^profile/?$', profile, name="myuw_profile_page"),
    re_path(r'^husky_experience_message/?$', husky_experience,
            name="myuw_husky_experience_message_page"),
    re_path(r'^husky_experience/?$', husky_experience,
            name="myuw_husky_experience_page"),
    re_path(r'^search/?$', search_res, name="myuw_search_res_page"),
    re_path(r'^teaching/(?P<year>2[0-9]{3}),(?P<quarter>[A-Za-z]+),'
            r'([1-9][0-9]?)$',
            teaching, name="myuw_teaching_page"),
    re_path(r'^teaching/(?P<year>2[0-9]{3}),(?P<quarter>[A-Za-z]+),'
            r'(?P<section>[\w& ]+,\d{3}\/[A-Z][A-Z0-9]?)$',
            teaching_section, name="myuw_section_page"),
    re_path(r'^teaching/(?P<year>2[0-9]{3}),(?P<quarter>[A-Za-z]+),'
            r'(?P<section>[\w& ]+,\d{3}\/[A-Z][A-Z0-9]?)'
            r'/students$',
            student_photo_list, name="myuw_photo_list"),
    re_path(r'^teaching/(?P<year>2[0-9]{3}),(?P<quarter>[a-z]+)$',
            teaching, name="myuw_teaching_page"),
    re_path(r'^teaching/?$', teaching, name="myuw_teaching_page"),
    re_path(r'^notices/?', notices, name="myuw_notices_page"),
    re_path(r'^thrive_messages/?', thrive_messages,
            name="myuw_thrive_messages_page"),
    re_path(r'^thrive/?', thrive, name="myuw_thrive_page"),
    re_path(r'^academic_calendar/?', academic_calendar,
            name="myuw_academic_calendar_page"),
    re_path(r'^future_quarters/(?P<quarter>2[0-9]{3},[-,a-z]+)',
            future_quarters, name="myuw_future_quarters_page"),
    re_path(
        r'^textbooks/(?P<term>2[0-9]{3},[-,a-z]+)/(?P<textbook>[%A-Z0-9]+)',
        textbooks, name="myuw_textbooks_page"),
    re_path(r'^textbooks/(?P<term>2[0-9]{3},[-,a-z]+)',
            textbooks, name="myuw_textbooks_page"),
    re_path(r'^textbooks/?',
            textbooks, name="myuw_textbooks_page"),
    re_path(r'resources/?', resources, name="myuw_resources_page"),
    re_path(r'^resource(/((?P<category>[a-z]+)?(/(?P<topic>[a-z]+))?)?)?',
            category, name="myuw_resource_page"),
    re_path(r'^logout', logout, name="myuw_logout"),
    re_path(r'lti/students$',
            LTIPhotoList.as_view(), name='myuw_lti_photo_list'),
    re_path(r'photo/(?P<url_key>.*)', show_photo),
    re_path(r'out/?', outbound_link, name='myuw_outbound_link'),
    re_path(r'.*', home, name="myuw_home"),
]
