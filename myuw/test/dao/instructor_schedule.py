from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from restclients.models.sws import Term, Section
from myuw.test import fdao_sws_override, fdao_pws_override, get_request,\
    get_request_with_user
from myuw.dao.instructor_schedule import is_instructor,\
    get_current_quarter_instructor_schedule,\
    get_limit_estimate_enrollment_for_section


@fdao_sws_override
@fdao_pws_override
class TestInstructorSchedule(TestCase):
    def test_is_instructor(self):
        now_request = get_request()
        get_request_with_user('bill', now_request)
        self.assertTrue(is_instructor(now_request))

    def test_get_current_quarter_instructor_schedule(self):
        now_request = get_request()
        get_request_with_user('bill', now_request)
        schedule = get_current_quarter_instructor_schedule(now_request)
        self.assertEqual(len(schedule.sections), 3)

    def test_get_limit_estimate_enrollment_for_section(self):
        term = Term()
        term.year = 2013
        term.quarter = 'spring'
        section = Section()
        section.term = term
        section.curriculum_abbr = 'TRAIN'
        section.course_number = 101
        section.section_id = 'A'

        limit = get_limit_estimate_enrollment_for_section(section)
        self.assertEqual(limit, 5)
