from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.models.sws import ClassSchedule, Term, Section, Person
from myuw.dao.term import get_current_quarter, get_next_quarter
from myuw.dao.schedule import _get_schedule,\
    has_summer_quarter_section, filter_schedule_sections_by_summer_term
from myuw.dao.schedule import get_schedule_by_term
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestSchedule(TestCase):
    def setUp(self):
        get_request()

    def test_has_summer_quarter_section(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2012
        term.quarter = "summer"
        schedule = _get_schedule(regid, term)
        self.assertTrue(has_summer_quarter_section(schedule))

        term = Term()
        term.year = 2012
        term.quarter = "autumn"
        self.assertRaises(DataFailureException,
                          _get_schedule,
                          regid, term)

    def test_filter_schedule_sections_by_summer_term(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2013
        term.quarter = "summer"
        schedule = _get_schedule(regid, term)
        # ensure it has both A and B terms
        has_a_term = False
        has_b_term = False
        for section in schedule.sections:
            if section.summer_term == "A-term":
                has_a_term = True
            if section.summer_term == "B-term":
                has_b_term = True
        self.assertTrue(has_a_term)
        self.assertTrue(has_b_term)

        filter_schedule_sections_by_summer_term(schedule, "A-term")
        # the B-term section no longer exists
        filtered_has_b_term = False
        filtered_has_a_term = False
        filtered_has_full_term = False
        for section in schedule.sections:
            if section.summer_term == "A-term":
                filtered_has_a_term = True
            if section.summer_term == "B-term":
                filtered_has_b_term = True
            if section.summer_term == "Full-term":
                filtered_has_full_term = True

        self.assertFalse(filtered_has_b_term)
        self.assertTrue(filtered_has_full_term)
        self.assertTrue(filtered_has_a_term)

    def test_winter_quarter_schedule(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"

        now_request = get_request_with_date("2013-11-30")
        cur_term = get_current_quarter(now_request)
        self.assertEqual(cur_term.year, 2013)
        self.assertEqual(cur_term.quarter, "autumn")

        next_term = get_next_quarter(now_request)
        self.assertEqual(next_term.year, 2014)
        self.assertEqual(next_term.quarter, "winter")
        self.assertFalse(cur_term == next_term)

        winter2014_sche = _get_schedule(regid, next_term)
        self.assertIsNotNone(winter2014_sche)
        self.assertEqual(len(winter2014_sche.sections), 5)

    def test_efs_before_end(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"

        now_request = get_request_with_date("2013-09-01")
        cur_term = get_current_quarter(now_request)
        self.assertEqual(cur_term.year, 2013)
        self.assertEqual(cur_term.quarter, "autumn")

        cur_term = get_current_quarter(now_request)
        fall_efs_schedule = _get_schedule(regid, cur_term)
        self.assertIsNotNone(fall_efs_schedule)
        self.assertEqual(len(fall_efs_schedule.sections), 2)

    def test_efs_after_end_of_early_start(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"

        now_request = get_request_with_date("2013-09-20")
        cur_term = get_current_quarter(now_request)
        self.assertEqual(cur_term.year, 2013)
        self.assertEqual(cur_term.quarter, "autumn")
        get_request_with_user('javerage', now_request)
        cur_term = get_current_quarter(now_request)
        fall_efs_schedule = get_schedule_by_term(now_request, cur_term)
        self.assertIsNotNone(fall_efs_schedule)
        self.assertEqual(len(fall_efs_schedule.sections), 1)
