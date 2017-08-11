from django.test import TestCase
from django.conf import settings
from restclients_core.exceptions import DataFailureException
from uw_sws.models import Term
from uw_sws.section import get_section_by_label
from myuw.dao.registration import _get_schedule, get_schedule_by_term,\
    get_active_registrations_for_section
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_user, get_request_with_date


@fdao_pws_override
@fdao_sws_override
class TestRegistrationsDao(TestCase):

    def test_data_failure_exception(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2014
        term.quarter = "autumn"
        self.assertRaises(DataFailureException,
                          _get_schedule,
                          regid, term)

    def test_get_schedule_by_term(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2013
        term.quarter = "autumn"
        schedule = _get_schedule(regid, term)
        self.assertIsNotNone(schedule)
        self.assertEqual(len(schedule.sections), 2)

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-04-01"))
        schedule = get_schedule_by_term(term)
        self.assertEqual(len(schedule.sections), 2)

    def test_get_active_registrations_for_section(self):
        section = get_section_by_label("2013,autumn,MUSEUM,700/A")
        regid = "10000000000000000000000000000011"
        registrations = get_active_registrations_for_section(section, regid)
        self.assertEqual(len(registrations), 1)
        enrolled_student = registrations[0].person
        self.assertEqual(enrolled_student.uwnetid, "javg001")
