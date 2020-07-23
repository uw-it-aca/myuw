from django.test import TestCase
from django.conf import settings
from restclients_core.exceptions import DataFailureException
from uw_sws.section import get_section_by_label
from myuw.dao.registration import get_schedule_by_term,\
    get_active_registrations_for_section
from myuw.dao.term import get_current_quarter
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_user, get_request_with_date


@fdao_pws_override
@fdao_sws_override
class TestRegistrationsDao(TestCase):

    def test_data_failure_exception(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2014-10-01"))
        term = get_current_quarter(request)
        self.assertRaises(DataFailureException,
                          get_schedule_by_term,
                          request, term)

    def test_get_schedule_by_term(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-10-01"))
        term = get_current_quarter(request)
        schedule = get_schedule_by_term(request, term)
        self.assertIsNotNone(schedule)
        self.assertEqual(len(schedule.sections), 2)
        self.assertEqual(schedule.sections[0].color_id, 1)
        self.assertEqual(schedule.sections[1].color_id, 2)

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-04-01"))
        term = get_current_quarter(request)
        schedule = get_schedule_by_term(request, term)
        self.assertEqual(len(schedule.sections), 5)

    def test_get_active_registrations_for_section(self):
        section = get_section_by_label("2013,autumn,MUSEUM,700/A")
        regid = "10000000000000000000000000000011"
        registrations = get_active_registrations_for_section(section, regid)
        self.assertEqual(len(registrations), 1)
        enrolled_student = registrations[0].person
        self.assertEqual(enrolled_student.uwnetid, "javg001")

        section = get_section_by_label('2017,autumn,EDC&I,552/A')
        self.assertEqual(section.section_label(), '2017,autumn,EDC&I,552/A')

        regid = "10000000000000000000000000000006"
        reg = get_active_registrations_for_section(section, regid)
        self.assertEqual(len(reg), 2)
        enrolled_student = reg[0].person
        self.assertEqual(enrolled_student.uwnetid, "javg003")

    def test_tsprint_false_instructor(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2014-01-01"))
        term = get_current_quarter(request)
        schedule = get_schedule_by_term(request, term)
        self.assertEqual(len(schedule.sections), 5)

        PHYS_122_a = schedule.sections[2]
        self.assertEqual(PHYS_122_a.section_label(),
                         "2014,winter,PHYS,122/A")
        self.assertEqual(len(PHYS_122_a.meetings), 2)

        meeting0_instructors = PHYS_122_a.meetings[0].instructors
        self.assertEqual(len(meeting0_instructors), 2)
        self.assertEqual(meeting0_instructors[0].display_name,
                         "SEATTLE GRADUATE STUDENT")
        self.assertEqual(meeting0_instructors[1].display_name,
                         "J. Average Student")

        meeting1_instructors = PHYS_122_a.meetings[1].instructors
        self.assertEqual(len(meeting1_instructors), 2)
        self.assertEqual(meeting1_instructors[0].display_name,
                         "SEATTLE GRADUATE STUDENT")
        self.assertEqual(meeting1_instructors[1].display_name,
                         "Seattle Faculty")

    def test_remote_section(self):
        request = get_request_with_user('eight',
                                        get_request_with_date("2020-10-01"))
        term = get_current_quarter(request)
        schedule = get_schedule_by_term(request, term)
        self.assertIsNotNone(schedule)
        self.assertEqual(len(schedule.sections), 1)
        self.assertTrue(schedule.sections[0].is_remote)
