from django.test import TestCase
from myuw_mobile.test.dao.course_color import TestCourseColors
from myuw_mobile.test.dao.registered_term import TestRegisteredTerm
from myuw_mobile.test.dao.schedule import TestSchedule
from myuw_mobile.test.dao.notice import TestNotce
from myuw_mobile.test.models import TestUserNotices
from myuw_mobile.test.academic_events import TestAcademicEvents
from myuw_mobile.test.dao.term import TestTerm
from myuw_mobile.test.dao.canvas import TestCanvas
from myuw_mobile.test.dao.card_display_dates import TestDisplayValues
from myuw_mobile.test.userservice_validation import TestValidation
from myuw_mobile.test.dao.hfs import TestHFS
from myuw_mobile.test.dao.library import TestLibrary
from myuw_mobile.test.dao.building import TestBuildings
from myuw_mobile.test.dao.category_links import TestCategoryLinks
from myuw_mobile.test.dao.finance import TestFinance
from myuw_mobile.test.dao.textbook import TestTextbooks
from myuw_mobile.test.dao.uwemail import TestUwEmail
from myuw_mobile.test.api.schedule import TestSchedule as APISchedule
from myuw_mobile.test.api.books import TestBooks
from myuw_mobile.test.api.hfs import TestHFS as TestHFSAPI
from myuw_mobile.test.api.profile import TestProfile
from myuw_mobile.test.api.library import TestLibrary as TestLibraryAPI
from myuw_mobile.test.api.category_links import TestLinks
from myuw_mobile.test.api.finance import TestFinance as TestFinanceAPI
from myuw_mobile.test.api.future_schedule import TestFutureSchedule
from myuw_mobile.test.api.other_quarters import TestOtherQuarters
from myuw_mobile.test.api.notices import TestNotices
from myuw_mobile.test.api.uwemail import TestUWEmail as TestUwEmailAPI
from myuw_mobile.test.api.academic_calendar import TestCalendarAPI
from myuw_mobile.test.template_tags import TestNetidHash
from myuw_mobile.test.context_processors import TestContextProcessors
from myuw_mobile.test.loggers import TestSessionLog
