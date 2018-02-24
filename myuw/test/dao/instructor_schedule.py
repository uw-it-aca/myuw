from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from uw_sws.models import Term, Section
from uw_sws.exceptions import InvalidSectionID
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user
from myuw.dao.instructor_schedule import is_instructor,\
    get_instructor_schedule_by_term, get_section_by_label,\
    get_limit_estimate_enrollment_for_section, _set_section_from_url,\
    get_instructor_section, get_primary_section, check_section_instructor
from myuw.dao.term import get_current_quarter
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.exceptions import NotSectionInstructorException
from userservice.user import UserServiceMiddleware


@fdao_sws_override
@fdao_pws_override
class TestInstructorSchedule(TestCase):
    def test_is_instructor(self):
        now_request = get_request_with_user('bill')
        self.assertTrue(is_instructor(now_request))

        now_request = get_request_with_user('billsea')
        self.assertTrue(is_instructor(now_request))

        now_request = get_request_with_user('billseata')
        self.assertTrue(is_instructor(now_request))

        now_request = get_request_with_user('billpce')
        self.assertTrue(is_instructor(now_request))

    def test_current_quarter_instructor_schedule(self):
        now_request = get_request_with_user('bill')
        term = get_current_quarter(now_request)
        schedule = get_instructor_schedule_by_term(now_request, term)
        self.assertEqual(len(schedule.sections), 6)

        request = get_request_with_user('billseata')
        UserServiceMiddleware().process_request(request)
        term = get_current_quarter(request)
        schedule = get_instructor_schedule_by_term(request, term)
        self.assertEqual(len(schedule.sections), 7)

    def test_set_section_from_url(self):
        # exclude course unpublished on Time Schedule
        sections = []
        section_url = "/student/v5/course/2018,spring,JAPAN,573/A.json"
        term = Term()
        term.year = 2018
        term.quarter = 'spring'
        term.time_schedule_published = {u'seattle': False}
        _set_section_from_url(sections, section_url, term)
        self.assertEqual(len(sections), 0)

        # include course published on Time Schedule
        term.time_schedule_published = {u'seattle': True}
        _set_section_from_url(sections, section_url, term)
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].section_label(),
                         "2018,spring,JAPAN,573/A")

        # PCE course not covered by time_schedule_published
        sections = []
        section_url = "/student/v5/course/2013,winter,BIGDATA,220/A.json"
        term = Term()
        term.year = 2013
        term.quarter = 'winter'
        term.time_schedule_published = {u'seattle': False,
                                        u'tacoma': False,
                                        u'bothell': False}
        _set_section_from_url(sections, section_url, term)
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].section_label(),
                         "2013,winter,BIGDATA,220/A")

    def test_get_instructor_section(self):
        req = get_request_with_user('bill')
        schedule = get_instructor_section(req, '2013,spring,ESS,102/A')
        self.assertEqual(len(schedule.sections), 1)

        req = get_request_with_user('billsea')
        schedule = get_instructor_section(req, '2017,autumn,CSE,154/A',
                                          include_registrations=True,
                                          include_linked_sections=True)
        self.assertEqual(len(schedule.sections), 5)
        self.assertEqual(schedule.sections[0].section_id, 'A')
        self.assertEqual(len(schedule.sections[0].registrations), 3)
        self.assertEqual(schedule.sections[1].section_id, 'AA')
        self.assertEqual(len(schedule.sections[1].registrations), 2)
        self.assertEqual(schedule.sections[2].section_id, 'AB')
        self.assertEqual(len(schedule.sections[2].registrations), 1)
        self.assertEqual(schedule.sections[3].section_id, 'AC')
        self.assertEqual(len(schedule.sections[3].registrations), 1)
        self.assertEqual(schedule.sections[4].section_id, 'AD')
        self.assertEqual(len(schedule.sections[4].registrations), 1)

    def test_invalid_instructor_section(self):
        req = get_request_with_user('bill')
        self.assertRaises(
            InvalidSectionID, get_instructor_section, req, None)
        self.assertRaises(
            InvalidSectionID, get_instructor_section, req, '12345')
        self.assertRaises(
            InvalidSectionID, get_instructor_section, req,
            '2013,spring,ESS,102')

    def test_get_instructor_secondary_section(self):
        req = get_request_with_user('billsea')
        schedule = get_instructor_section(req, '2017,autumn,CSE,154/AA')
        self.assertEqual(len(schedule.sections), 1)
        schedule = get_instructor_section(req, '2017,autumn,EDC&I,552/A')
        self.assertEqual(len(schedule.sections), 1)

    def test_check_instructor_section(self):
        req = get_request_with_user('bill')
        schedule = get_instructor_section(req, '2013,spring,ESS,102/A')
        ess_section = schedule.sections[0]

        bill = get_person_of_current_user(req)
        self.assertIsNone(check_section_instructor(ess_section, bill))

        req = get_request_with_user('billsea')
        schedule = get_instructor_section(req, '2017,autumn,CSE,154/AA')
        cse_section = schedule.sections[0]

        billsea = get_person_of_current_user(req)
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
        term = get_current_quarter(request)
        schedule = get_instructor_schedule_by_term(request, term)
        self.assertEqual(len(schedule.sections), 1)
        self.assertEqual(schedule.sections[0].current_enrollment, 3)

    def test_get_primary_section(self):
        secondary_section = get_section_by_label('2017,autumn,CSE,154/AA')
        section = get_primary_section(secondary_section)
        self.assertEqual(secondary_section.primary_section_label(),
                         section.section_label())
