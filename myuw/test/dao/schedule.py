from django.test import TestCase
from django.conf import settings
from restclients_core.exceptions import DataFailureException
from uw_sws.models import ClassSchedule, Term, Section, Person
from myuw.dao.term import get_current_quarter, get_next_quarter
from myuw.dao.schedule import get_current_quarter_schedule,\
    get_next_quarter_schedule, get_next_autumn_quarter_schedule,\
    has_summer_quarter_section, filter_schedule_sections_by_summer_term
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestSchedule(TestCase):

    def test_filter_schedule_sections_by_summer_term(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-04-01"))
        schedule = get_next_quarter_schedule(request)
        self.assertTrue(has_summer_quarter_section(schedule))

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

    def test_spring_quarter_schedule(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-04-01"))
        schedule = get_current_quarter_schedule(request)
        self.assertIsNotNone(schedule)
        self.assertEqual(len(schedule.sections), 5)

    def test_multi_enrollments_for_a_course(self):
        request = get_request_with_user('seagrad',
                                        get_request_with_date("2017-04-01"))
        schedule = get_current_quarter_schedule(request)
        self.assertIsNotNone(schedule)
        self.assertEqual(len(schedule.sections), 2)

    def test_winter_quarter_schedule(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-09-01"))
        schedule = get_next_quarter_schedule(request)
        self.assertIsNotNone(schedule)
        self.assertEqual(len(schedule.sections), 5)

    def test_efs_before_end(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-04-01"))
        fall_efs_schedule = get_next_autumn_quarter_schedule(request)
        self.assertIsNotNone(fall_efs_schedule)
        self.assertEqual(len(fall_efs_schedule.sections), 2)
