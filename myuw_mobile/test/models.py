from django.test import TestCase
from django.conf import settings

from myuw_mobile.models import UserNotices, DepartmentCalendar
from myuw_mobile.dao.notice import get_notices_by_regid


class TestUserNotices(TestCase):
    def test_hash(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = get_notices_by_regid(regid)


        notice = notices[0]

        model = UserNotices()

        hash = model.generate_hash(notice)

        self.assertEquals(hash, "516660a8fb896ebc046ca68c8e8bcd02")

class TestCalendarModel(TestCase):
    def test_base_url(self):
        cal = DepartmentCalendar()
        cal.set_base_url('')
        self.assertIsNone(cal.base_url)

        cal2 = DepartmentCalendar()
        cal2.set_base_url('http://asdf.com/')
        self.assertEqual(cal2.base_url, "http://asdf.com/")
