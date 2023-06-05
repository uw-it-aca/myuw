# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TransactionTestCase
from unittest.mock import patch
from datetime import datetime, date
from django.utils import timezone
from restclients_core.exceptions import DataFailureException
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.myuw_notice import (
    get_myuw_notices_for_user, get_last_sunday, get_start_date,
    get_current_quarter, campus_neutral, is_stud_campus_matched,
    is_employee_campus_matched, get_first_day_quarter,
    get_notices_by_date, get_notices_by_term, student_affiliation_matched)
from myuw.dao.notice_mapping import categorize_notices
from myuw.test import get_request_with_user, get_request_with_date
from myuw.models.myuw_notice import MyuwNotice


def get_datetime_with_tz(year, month, day, hour):
    return timezone.make_aware(datetime(year, month, day, hour, 0, 0))


class TestMyuwNotice(TransactionTestCase):

    def test_get_last_sunday(self):
        start_sun = get_last_sunday(date(2013, 1, 2))
        self.assertEqual(str(start_sun), "2012-12-30")
        start_sun = get_last_sunday(date(2013, 1, 5))
        self.assertEqual(str(start_sun), "2012-12-30")
        start_sun = get_last_sunday(date(2013, 1, 6))
        self.assertEqual(str(start_sun), "2013-01-06")
        start_sun = get_last_sunday(date(2013, 9, 25))
        self.assertEqual(str(start_sun), "2013-09-22")

    def test_get_start_date(self):
        dt = get_start_date(date(2013, 1, 6), -1)
        self.assertEqual(str(dt), "2012-12-30")
        dt = get_start_date(date(2013, 1, 6), 0)
        self.assertEqual(str(dt), "2013-01-06")
        dt = get_start_date(date(2013, 1, 6), 1)
        self.assertEqual(str(dt), "2013-01-13")
        dt = get_start_date(date(2013, 9, 22), -2)
        self.assertEqual(str(dt), "2013-09-08")

    def test_get_first_day_quarter(self):
        notice = MyuwNotice(title="Test",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start_week=-2,
                            duration=1,
                            is_summer_b=True)
        request = get_request_with_date("2013-07-11")
        cur_term = get_current_quarter(request)
        self.assertEqual(cur_term.quarter, "summer")
        dt = get_first_day_quarter(cur_term, notice)
        self.assertEqual(str(dt), "2013-07-25")

        notice = MyuwNotice(title="Test",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start_week=-2,
                            duration=1,
                            is_autumn=True)
        request = get_request_with_date("2013-09-01")
        cur_term = get_current_quarter(request)
        self.assertEqual(cur_term.quarter, "autumn")
        dt = get_first_day_quarter(cur_term, notice)
        self.assertEqual(str(dt), "2013-09-25")

    def test_get_notices_by_term(self):
        notice = MyuwNotice(title="Test1",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start_week=2,
                            duration=1,
                            is_summer_a=True)
        notice.save()
        notice = MyuwNotice(title="Test2",
                            content="Notice Content Five",
                            notice_type="Banner",
                            start_week=-2,
                            duration=1,
                            is_summer_b=True)
        notice.save()
        notice = MyuwNotice(title="Test3",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start_week=-2,
                            duration=11,
                            is_autumn=True)
        notice.save()
        request = get_request_with_date("2013-07-08")
        notices = get_notices_by_term(request)
        self.assertEqual(len(notices), 2)
        self.assertEqual(notices[0].title, "Test1")
        self.assertEqual(notices[1].title, "Test2")

        request = get_request_with_date("2013-08-25")
        notices = get_notices_by_term(request)
        self.assertEqual(len(notices), 0)

        request = get_request_with_date("2013-09-08")
        notices = get_notices_by_term(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Test3")

    def test_get_notices_by_date(self):
        notice = MyuwNotice(title="Foo",
                            content="Notice Content",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 5, 8, 10),
                            end=get_datetime_with_tz(2018, 5, 15, 10),
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
        request = get_request_with_date("2018-05-13")
        notices = get_notices_by_date(request)
        self.assertEqual(len(notices), 2)

        request = get_request_with_date("2018-05-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Foo")

    def test_by_campus(self):
        affiliation1 = {"seattle": True, "bothell": False, "tacoma": False}
        affiliation2 = {"seattle": False, "bothell": True, "tacoma": False}
        affiliation3 = {"seattle": False, "bothell": False, "tacoma": True}
        affiliation4 = {"official_seattle": True,
                        "official_bothell": False,
                        "official_tacoma": False}
        affiliation5 = {"official_seattle": False,
                        "official_bothell": True,
                        "official_tacoma": False}
        affiliation6 = {"official_seattle": False,
                        "official_bothell": False,
                        "official_tacoma": True}
        notice = MyuwNotice(title="Campus neutral",
                            content="Notice Content Three",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 10, 10),
                            is_seattle=False,
                            is_bothell=False,
                            is_tacoma=False)
        self.assertTrue(campus_neutral(notice))
        self.assertTrue(is_stud_campus_matched(notice, affiliation1))
        self.assertTrue(is_stud_campus_matched(notice, affiliation2))
        self.assertTrue(is_stud_campus_matched(notice, affiliation3))
        self.assertTrue(is_employee_campus_matched(notice, affiliation4))
        self.assertTrue(is_employee_campus_matched(notice, affiliation5))
        self.assertTrue(is_employee_campus_matched(notice, affiliation6))

        notice = MyuwNotice(title="Seattle",
                            content="Notice Content Three",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 10, 10),
                            is_seattle=True)
        self.assertFalse(campus_neutral(notice))
        self.assertTrue(is_stud_campus_matched(notice, affiliation1))
        self.assertFalse(is_stud_campus_matched(notice, affiliation2))
        self.assertFalse(is_stud_campus_matched(notice, affiliation3))
        self.assertTrue(is_employee_campus_matched(notice, affiliation4))
        self.assertFalse(is_employee_campus_matched(notice, affiliation5))
        self.assertFalse(is_employee_campus_matched(notice, affiliation6))

        notice = MyuwNotice(title="Bothell",
                            content="Notice Content Four",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 20, 10),
                            is_bothell=True)
        self.assertFalse(campus_neutral(notice))
        self.assertFalse(is_stud_campus_matched(notice, affiliation1))
        self.assertTrue(is_stud_campus_matched(notice, affiliation2))
        self.assertFalse(is_stud_campus_matched(notice, affiliation3))
        self.assertFalse(is_employee_campus_matched(notice, affiliation4))
        self.assertTrue(is_employee_campus_matched(notice, affiliation5))
        self.assertFalse(is_employee_campus_matched(notice, affiliation6))

        notice = MyuwNotice(title="Tacoma",
                            content="Notice Content Four",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2018, 6, 8, 10),
                            end=get_datetime_with_tz(2018, 6, 20, 10),
                            is_tacoma=True)
        self.assertFalse(campus_neutral(notice))
        self.assertFalse(is_stud_campus_matched(notice, affiliation1))
        self.assertFalse(is_stud_campus_matched(notice, affiliation2))
        self.assertTrue(is_stud_campus_matched(notice, affiliation3))
        self.assertFalse(is_employee_campus_matched(notice, affiliation4))
        self.assertFalse(is_employee_campus_matched(notice, affiliation5))
        self.assertTrue(is_employee_campus_matched(notice, affiliation6))

    def test_is_affiliations(self):
        notice = MyuwNotice(title="For all users",
                            content="For all users",
                            notice_type="Banner",
                            notice_category="All",
                            start=get_datetime_with_tz(2013, 6, 8, 10),
                            end=get_datetime_with_tz(2013, 6, 20, 10),
                            is_seattle=False,
                            is_bothell=False,
                            is_tacoma=False)
        notice.save()

        notice = MyuwNotice(title="For all instructors",
                            content="For all instructors",
                            notice_type="Banner",
                            notice_category="Instructor",
                            start=get_datetime_with_tz(2013, 6, 8, 10),
                            end=get_datetime_with_tz(2013, 6, 20, 10),
                            is_instructor=True)
        notice.save()
        notice = MyuwNotice(title="For all student",
                            content="For all student",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2013, 6, 8, 10),
                            end=get_datetime_with_tz(2013, 6, 20, 10),
                            is_student=True)
        notice.save()
        notice = MyuwNotice(title="For bothell intl students",
                            content="For bothell Intl students",
                            notice_type="Banner",
                            notice_category="Student",
                            start=get_datetime_with_tz(2013, 6, 8, 10),
                            end=get_datetime_with_tz(2013, 6, 20, 10),
                            is_bothell=True,
                            is_intl_stud=True)
        notice.save()
        notice = MyuwNotice(title="For Seattle staff",
                            content="For Seattle staff",
                            notice_type="Banner",
                            notice_category="Employee",
                            start=get_datetime_with_tz(2013, 6, 8, 10),
                            end=get_datetime_with_tz(2013, 6, 20, 10),
                            is_seattle=True,
                            is_staff_employee=True)
        notice.save()
        notice = MyuwNotice(title="For alumni",
                            content="For alumni",
                            notice_type="Banner",
                            notice_category="Alumni",
                            start=get_datetime_with_tz(2013, 6, 8, 10),
                            end=get_datetime_with_tz(2013, 6, 20, 10),
                            is_alumni=True)
        notice.save()

        request = get_request_with_date("2013-06-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 2)
        self.assertEqual(notices[0].title, "For all users")
        self.assertEqual(notices[1].title, "For all student")

        request = get_request_with_date("2013-06-09")
        get_request_with_user('staff', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 2)
        self.assertEqual(notices[0].title, "For all users")
        self.assertEqual(notices[1].title, "For Seattle staff")

        request = get_request_with_date("2013-06-09")
        get_request_with_user('botgrad', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 3)
        self.assertEqual(notices[0].title, "For all users")
        self.assertEqual(notices[1].title, "For all student")
        self.assertEqual(notices[2].title, "For bothell intl students")

        request = get_request_with_date("2013-06-09")
        get_request_with_user('jalum', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 2)
        self.assertEqual(notices[0].title, "For all users")
        self.assertEqual(notices[1].title, "For alumni")

        request = get_request_with_user(
            'none', get_request_with_date("2013-06-09"))
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "For all users")

    def test_not_affiliations(self):
        notice = MyuwNotice(
            title="For seattle students except intl students",
            content="test case",
            notice_type="Banner",
            notice_category="MyUWNotice",
            is_critical=False,
            start=None,
            end=None,
            start_week=0,
            duration=10,
            is_winter=True,
            is_spring=True,
            is_seattle=True,
            is_student=True,
            not_intl_stud=True)
        notice.save()
        request = get_request_with_date("2013-04-01")
        request = get_request_with_user('jinter', request)
        affiliations = get_all_affiliations(request)
        self.assertFalse(student_affiliation_matched(notice, affiliations))

    def test_myuwnotice_mapping(self):
        notice = MyuwNotice(title="Test",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start=get_datetime_with_tz(2013, 6, 8, 10),
                            end=get_datetime_with_tz(2013, 6, 20, 10),
                            is_student=True)
        categorized = categorize_notices([notice])
        self.assertEqual(len(categorized), 1)
        self.assertEqual(categorized[0].location_tags, ['notice_banner'])

    def test_target_group(self):
        notice = MyuwNotice(title="Goo",
                            content="Notice Content",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start=get_datetime_with_tz(2018, 5, 8, 10),
                            end=get_datetime_with_tz(2018, 5, 10, 10),
                            target_group='u_astratst_myuw_test-support-admin')
        notice.save()
        notice = MyuwNotice(title="Goo1",
                            content="Notice Content1",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start=get_datetime_with_tz(2018, 5, 8, 10),
                            end=get_datetime_with_tz(2018, 5, 10, 10),
                            target_group='u_not_exist')
        notice.save()
        request = get_request_with_user(
            'bill', get_request_with_date("2018-05-09"))
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Goo")

        request = get_request_with_user(
            'jalum', get_request_with_date("2018-05-09"))
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 0)

    @patch('myuw.dao.myuw_notice.is_effective_member', spec=True)
    def test_target_group_err(self, mock):
        notice = MyuwNotice(title="Goo",
                            content="Notice Content",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start=get_datetime_with_tz(2018, 5, 8, 10),
                            end=get_datetime_with_tz(2018, 5, 10, 10),
                            target_group='u_astratst_myuw_test-support-admin')
        notice.save()
        mock.side_effect = DataFailureException(
            None, 401, "No read permission")
        request = get_request_with_user(
            'bill', get_request_with_date("2018-05-09"))
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 0)
