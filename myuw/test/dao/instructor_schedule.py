from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from uw_sws.models import Term, Section
from uw_pws import PWS
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user, get_request
from myuw.dao.instructor_schedule import is_instructor,\
    get_current_quarter_instructor_schedule,\
    get_instructor_schedule_by_term, get_section_by_label,\
    get_limit_estimate_enrollment_for_section,\
    get_instructor_section, get_primary_section, check_section_instructor
from myuw.dao.term import get_current_quarter
from myuw.dao.exceptions import NotSectionInstructorException
from userservice.user import UserServiceMiddleware


@fdao_sws_override
@fdao_pws_override
class TestInstructorSchedule(TestCase):
    def test_is_instructor(self):
        now_request = get_request()
        get_request_with_user('bill', now_request)
        self.assertTrue(is_instructor(now_request))

        get_request_with_user('billsea', now_request)
        self.assertTrue(is_instructor(now_request))

        get_request_with_user('billseata', now_request)
        self.assertTrue(is_instructor(now_request))

        get_request_with_user('billpce', now_request)
        self.assertTrue(is_instructor(now_request))

    def test_get_current_quarter_instructor_schedule(self):
        now_request = get_request()
        get_request_with_user('bill', now_request)
        schedule = get_current_quarter_instructor_schedule(now_request)
        self.assertEqual(len(schedule.sections), 6)

        request = get_request_with_user('billseata',
                                        get_request())
        UserServiceMiddleware().process_request(request)
        term = get_current_quarter(request)
        schedule = get_instructor_schedule_by_term(term)
        self.assertEqual(len(schedule.sections), 7)

    def test_get_instructor_section(self):
        person = person = PWS().get_person_by_netid('bill')
        schedule = get_instructor_section(
            person, '2013', 'spring', 'ESS', '102', 'A')
        self.assertEqual(len(schedule.sections), 1)

    def test_get_instructor_secondary_section(self):
        person = PWS().get_person_by_netid('billsea')

        schedule = get_instructor_section(
            person, '2017', 'autumn', 'CSE', '154', 'AA')
        self.assertEqual(len(schedule.sections), 1)

        schedule = get_instructor_section(
            person, '2017', 'autumn', 'EDC&I', '552', 'A')
        self.assertEqual(len(schedule.sections), 1)

    def test_check_instructor_section(self):
        bill = PWS().get_person_by_netid('bill')
        schedule = get_instructor_section(
            bill, '2013', 'spring', 'ESS', '102', 'A')
        ess_section = schedule.sections[0]
        self.assertEqual(None, check_section_instructor(ess_section, bill))

        billsea = PWS().get_person_by_netid('billsea')
        schedule = get_instructor_section(
            billsea, '2017', 'autumn', 'CSE', '154', 'AA')
        cse_section = schedule.sections[0]
        self.assertEqual(None, check_section_instructor(cse_section, billsea))

        self.assertRaises(NotSectionInstructorException,
                          check_section_instructor, ess_section, billsea)
        self.assertRaises(NotSectionInstructorException,
                          check_section_instructor, cse_section, bill)

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

    def test_pce_instructor_schedule(self):
        request = get_request_with_user('billpce',
                                        get_request_with_date("2013-10-01"))
        schedule = get_current_quarter_instructor_schedule(request)
        self.assertEqual(len(schedule.sections), 1)
        self.assertEqual(schedule.sections[0].current_enrollment, 3)

    def test_get_primary_section(self):
        secondary_section = get_section_by_label('2017,autumn,CSE,154/AA')
        section = get_primary_section(secondary_section)
        self.assertEqual(secondary_section.primary_section_label(),
                         section.section_label())
