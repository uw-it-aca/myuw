from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from myuw.test import get_request, get_request_with_user
from uw_sws.models import Term, Section
from myuw.test import fdao_sws_override, fdao_pws_override
from myuw.dao.instructor_schedule import is_instructor,\
    get_current_quarter_instructor_schedule,\
    get_limit_estimate_enrollment_for_section,\
    get_instructor_section
from userservice.user import UserServiceMiddleware


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
        self.assertEqual(len(schedule.sections), 6)

    def test_get_instructor_section(self):
        now_request = RequestFactory().get("/")
        now_request.session = {}

        user = User.objects.create_user(username='bill',
                                        email='bill@example.com',
                                        password='')
        now_request.user = user
        UserServiceMiddleware().process_request(now_request)
        schedule = get_instructor_section('2013', 'spring', 'ESS', '102', 'A')
        self.assertEqual(len(schedule.sections), 1)

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
