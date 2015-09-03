from django.test import TestCase
from myuw.test.dao.course_color import TestCourseColors
from myuw.test.dao.registered_term import TestRegisteredTerm
from myuw.test.dao.schedule import TestSchedule
from myuw.test.dao.notice_mapping import TestMapNotices
from myuw.test.dao.notice_categorization import TestNoticeCategories
from myuw.test.dao.notice import TestNotices
from myuw.test.models import TestUserNotices
from myuw.test.academic_events import TestAcademicEvents
from myuw.test.dao.term import TestTerm
from myuw.test.dao.term_current import TestTermCurrent
from myuw.test.dao.term_specific import TestTermSpecific
from myuw.test.dao.canvas import TestCanvas
from myuw.test.dao.card_display_dates import TestDisplayValues
from myuw.test.userservice_validation import TestValidation
from myuw.test.dao.hfs import TestHFS
from myuw.test.dao.library import TestLibrary
from myuw.test.dao.building import TestBuildings
from myuw.test.dao.category_links import TestCategoryLinks
from myuw.test.dao.finance import TestFinance
from myuw.test.dao.textbook import TestTextbooks
from myuw.test.dao.uwemail import TestUwEmail
from myuw.test.api.schedule import TestSchedule as APISchedule
from myuw.test.api.books import TestBooks
from myuw.test.api.cur_books import TestCurBooks
from myuw.test.api.hfs import TestHFS as TestHFSAPI
from myuw.test.api.profile import TestProfile
from myuw.test.api.library import TestLibrary as TestLibraryAPI
from myuw.test.api.category_links import TestLinks
from myuw.test.api.finance import TestFinance as TestFinanceAPI
from myuw.test.api.future_schedule import TestFutureSchedule
from myuw.test.api.other_quarters import TestOtherQuarters
from myuw.test.api.notices import TestNotices
from myuw.test.api.uwemail import TestUWEmail as TestUwEmailAPI
from myuw.test.api.academic_calendar import TestCalendarAPI
from myuw.test.template_tags import TestNetidHash
from myuw.test.context_processors import TestContextProcessors
from myuw.test.views.mobile_login import TestLoginRedirects
from myuw.test.views.rest_dispatch import TestDispatchErrorCases
from myuw.test.loggers import TestSessionLog
from myuw.test.dao.calendar_mapping import TestCalendarMapping
from myuw.test.dao.calendar import TestCalendar
from myuw.test.cache import TestCustomCachePolicy
