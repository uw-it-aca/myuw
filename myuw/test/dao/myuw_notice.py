# -*- coding: utf8 -*-
from django.test import TransactionTestCase
from datetime import datetime
import pytz
from django.utils import timezone
from myuw.dao.myuw_notice import get_myuw_notices_for_user
from myuw.dao.notice_mapping import categorize_notices
from myuw.test import get_request_with_user, get_request_with_date
from myuw.models.myuw_notice import MyuwNotice


def get_datetime_with_tz(year, month, day, hour):
    local_tz = timezone.get_current_timezone()
    return local_tz.localize(
        datetime(year, month, day, hour, 0, 0)).astimezone(pytz.utc)


class TestMyuwNotice(TransactionTestCase):

    def test_by_date(self):
        notice = MyuwNotice(title="Foo",
                            content="Notice Content",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 5, 8, 10),
                            end=get_datetime_with_tz(2018, 5, 10, 10),
                            is_seattle=True)
        notice.save()
        self.assertIsNotNone(str(notice))
        notice = MyuwNotice(title="Bar",
                            content="Notice Content Two",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 5, 12, 10),
                            end=get_datetime_with_tz(2018, 5, 20, 10),
                            is_seattle=True)
        notice.save()

        request = get_request_with_date("2018-05-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Foo")

    def test_by_campus(self):
        notice = MyuwNotice(title="Baz",
                            content="Notice Content Three",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 10, 10),
                            is_seattle=True)
        notice.save()
        notice = MyuwNotice(title="Alert",
                            content="Notice Content Four",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 20, 10),
                            is_bothell=True)
        notice.save()
        request = get_request_with_date("2018-06-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Baz")

    def test_no_campus(self):
        notice = MyuwNotice(title="Alert",
                            content="Notice Content Four",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 20, 10))
        notice.save()
        request = get_request_with_date("2018-06-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Alert")

    def test_affil(self):
        notice = MyuwNotice(title="Alert",
                            content="Notice Content Four",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 20, 10),
                            is_instructor=True)
        notice.save()
        notice = MyuwNotice(title="All Student",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 20, 10),
                            is_student=True)
        notice.save()
        notice = MyuwNotice(title="Seattle Intl",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 20, 10),
                            is_seattle=True,
                            is_intl_stud=True)
        notice.save()
        request = get_request_with_date("2018-06-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "All Student")

        request = get_request_with_date("2018-06-09")
        get_request_with_user('jinter', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 2)
        self.assertEqual(notices[0].title, "All Student")
        self.assertEqual(notices[1].title, "Seattle Intl")

        request = get_request_with_date("2018-06-09")
        get_request_with_user('jbothell', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "All Student")

    def test_no_affil(self):
            notice = MyuwNotice(title="Alert",
                                content="Notice Content Four",
                                notice_type="Banner",
                                notice_category="Student",
                                start=get_datetime_with_tz(2018, 6, 8, 10),
                                end=get_datetime_with_tz(2018, 6, 20, 10))
            notice.save()
            notice = MyuwNotice(title="Test",
                                content="Notice Content Five",
                                notice_type="Banner",
                                notice_category="Student",
                                start=get_datetime_with_tz(2018, 6, 8, 10),
                                end=get_datetime_with_tz(2018, 6, 20, 10),
                                is_student=True)
            notice.save()
            request = get_request_with_date("2018-06-09")
            get_request_with_user('javerage', request)
            notices = get_myuw_notices_for_user(request)
            self.assertEqual(len(notices), 2)

    def test_myuwnotice_mapping(self):
        notice = MyuwNotice(title="Test",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 20, 10),
                            is_student=True)
        categorized = categorize_notices([notice])
        self.assertEqual(len(categorized), 1)
        self.assertEqual(categorized[0].location_tags, ['notice_banner'])
