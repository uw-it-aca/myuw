from myuw.test.models import TestUserNotices
from myuw.test.academic_events import TestAcademicEvents
from myuw.test.dao import TestDaoInit
from myuw.test.dao.calendar_mapping import TestCalendarMapping
from myuw.test.dao.calendar import TestCalendar
from myuw.test.dao.notice_mapping import TestMapNotices
from myuw.test.dao.notice_categorization import TestNoticeCategories
from myuw.test.dao.notice import TestNotices
from myuw.test.dao.building import TestBuildings
from myuw.test.dao.finance import TestFinance
from myuw.test.dao.card_display_dates import TestDisplayValues
from myuw.test.dao.grad import TestDaoGrad
from myuw.test.dao.hfs import TestHFS as TestDaoHFS
from myuw.test.dao.iasystem import IASystemDaoTest
from myuw.test.dao.mailman import TestMailmanDao
from myuw.test.dao.password import TestDaoPassword
from myuw.test.dao.textbook import TestTextbooks
from myuw.test.dao.thrive import TestThrive
from myuw.test.dao.emaillink import TestEmailServiceUrl
from myuw.test.api.books import TestApiBooks
from myuw.test.api.cur_books import TestApiCurBooks
from myuw.test.api.hfs import TestHFS as TestHFSAPI
from myuw.test.api.profile import TestProfile
from myuw.test.api.emaillist import TestEmaillistApi
from myuw.test.api.category_links import TestLinks
from myuw.test.api.finance import TestFinance as TestFinanceAPI
from myuw.test.api.notices import TestNotices as TestNoticesAPI
from myuw.test.api.upass import TestUpassApi
from myuw.test.api.thrive import TestApiThrive
from myuw.test.api.academic_calendar import TestCalendarAPI
from myuw.test.api.dept_calendar import TestDeptCalAPI
from myuw.test.views.teaching import TestTeachingMethods
from myuw.test.views.logout import TestLogoutLink
from myuw.test.views.mobile_login import TestLogins
from myuw.test.views.test_api import TestDispatchErrorCases
from myuw.test.views.textbooks import TestTextbook
from myuw.test.speed import TestPageSpeeds
