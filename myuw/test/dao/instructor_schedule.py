from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from restclients.models.sws import Term, Section
from myuw.dao.instructor_schedule import is_instructor,\
    get_current_quarter_instructor_schedule,\
    get_limit_estimate_enrollment_for_section
from userservice.user import UserServiceMiddleware


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestInstructorSchedule(TestCase):
    def test_is_instructor(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}

            user = User.objects.create_user(username='bill',
                                            email='bill@example.com',
                                            password='')
            now_request.user = user
            UserServiceMiddleware().process_request(now_request)
            self.assertTrue(is_instructor(now_request))

    def test_get_current_quarter_instructor_schedule(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}

            user = User.objects.create_user(username='bill',
                                            email='bill@example.com',
                                            password='')
            now_request.user = user
            UserServiceMiddleware().process_request(now_request)
            schedule = get_current_quarter_instructor_schedule(now_request)
            self.assertEqual(len(schedule.sections), 2)

    def test_get_limit_estimate_enrollment_for_section(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
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
