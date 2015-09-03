from datetime import datetime
from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from restclients.models.sws import ClassSchedule, Term, Section, Person
from myuw.dao.term.current import get_next_non_summer_quarter,\
    get_next_autumn_quarter, term_matched, is_in_summer_a_term,\
    get_eof_last_instruction, get_bof_7d_before_last_instruction,\
    get_bof_1st_instruction, get_eof_7d_after_class_start,\
    get_eof_term, get_eof_last_final_exam
from myuw.dao.term.specific import get_specific_quarter


FDAO_SWS = 'restclients.dao_implementation.sws.File'
LDAO_SWS = 'restclients.dao_implementation.sws.Live'


class TestTermCurrent(TestCase):
    def test_get_next_non_summer_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-01"
            quarter = get_next_non_summer_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

    def test_get_next_autumn_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-01"
            quarter = get_next_autumn_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

    def testget_specific_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            quarter = get_specific_quarter(2013, 'spring')
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')
            quarter = get_specific_quarter(2013, 'autumn')
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

    def test_term_matched(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertTrue(term_matched(now_request, 'A-term'))
            self.assertFalse(term_matched(now_request, 'Full-term'))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertTrue(term_matched(now_request, 'B-term'))
            self.assertTrue(term_matched(now_request, 'Full-term'))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-10"
            self.assertTrue(term_matched(now_request, 'None'))
            self.assertTrue(term_matched(now_request, '-'))

    def test_is_in_summer_a_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertTrue(is_in_summer_a_term(now_request))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertFalse(is_in_summer_a_term(now_request))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-10"
            self.assertFalse(is_in_summer_a_term(now_request))

    def test_get_eof_last_instruction(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-05-10"
            self.assertEqual(get_eof_last_instruction(now_request),
                             datetime(2013, 6, 8, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertEqual(get_eof_last_instruction(now_request, True),
                             datetime(2013, 7, 25, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertEqual(get_eof_last_instruction(now_request),
                             datetime(2013, 8, 24, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertEqual(get_eof_last_instruction(now_request, True),
                             datetime(2013, 8, 24, 0, 0, 0))

    def test_bof_7d_before_last_instruction(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-05-10"
            self.assertEqual(get_bof_7d_before_last_instruction(now_request),
                             datetime(2013, 5, 31, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertEqual(get_bof_7d_before_last_instruction(now_request),
                             datetime(2013, 7, 17, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertEqual(get_bof_7d_before_last_instruction(now_request),
                             datetime(2013, 8, 16, 0, 0, 0))

    def test_bof_1st_instruction(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-05-10"
            self.assertEqual(get_bof_1st_instruction(now_request),
                             datetime(2013, 4, 1, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertEqual(get_bof_1st_instruction(now_request),
                             datetime(2013, 6, 24, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertEqual(get_bof_1st_instruction(now_request),
                             datetime(2013, 6, 24, 0, 0, 0))

    def test_eof_7d_after_class_start(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-05-10"
            self.assertEqual(get_eof_7d_after_class_start(now_request),
                             datetime(2013, 4, 9, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertEqual(get_eof_7d_after_class_start(now_request),
                             datetime(2013, 7, 2, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertEqual(get_eof_7d_after_class_start(now_request),
                             datetime(2013, 7, 2, 0, 0, 0))

    def test_eof_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-10"
            self.assertEqual(get_eof_term(now_request),
                             datetime(2013, 3, 27, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertEqual(get_eof_term(now_request, True),
                             datetime(2013, 7, 25, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertEqual(get_eof_term(now_request),
                             datetime(2013, 8, 28, 0, 0, 0))

    def test_eof_last_final_exam(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-10"
            self.assertEqual(get_eof_last_final_exam(now_request),
                             datetime(2013, 3, 23, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertEqual(get_eof_last_final_exam(now_request, True),
                             datetime(2013, 7, 25, 0, 0, 0))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertEqual(get_eof_last_final_exam(now_request),
                             datetime(2013, 8, 24, 0, 0, 0))
