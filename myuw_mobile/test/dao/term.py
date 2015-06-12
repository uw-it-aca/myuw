from datetime import datetime
from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from restclients.models.sws import ClassSchedule, Term, Section, Person
from myuw_mobile.dao.term import _get_term_by_year_and_quarter, is_past,\
    is_using_file_dao, get_default_date, get_comparison_date,\
    get_current_quarter, get_next_quarter, get_next_non_summer_quarter,\
    get_next_autumn_quarter, _get_term_by_year_and_quarter, get_quarter,\
    is_past, is_a_term, is_b_term, is_half_summer_term, is_full_summer_term,\
    is_same_summer_term, term_matched, is_current_summer_a_term,\
    get_eof_last_instruction, get_bof_7d_before_last_instruction,\
    get_bof_1st_instruction, get_eof_7d_after_class_start,\
    get_eof_term, get_eof_last_final_exam


FDAO_SWS = 'restclients.dao_implementation.sws.File'
LDAO_SWS = 'restclients.dao_implementation.sws.Live'


class TestTerm(TestCase):

    def test_get_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            term = _get_term_by_year_and_quarter(2013, "summer")
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, "summer")
            now_request = RequestFactory().get("/")
            now_request.session = {}
            self.assertFalse(is_past(term, now_request))

    def test_is_past(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            term = _get_term_by_year_and_quarter(2014, "winter")
            self.assertEqual(term.year, 2014)
            self.assertEqual(term.quarter, "winter")
            now_request = RequestFactory().get("/")
            now_request.session = {}
            self.assertFalse(is_past(term, now_request))

            term = _get_term_by_year_and_quarter(2013, "winter")
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, "winter")
            now_request = RequestFactory().get("/")
            now_request.session = {}
            self.assertTrue(is_past(term, now_request))

    def test_default_date(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            date = get_default_date()
            self.assertEquals(date.year, 2013)
            self.assertEquals(date.month, 4)
            self.assertEquals(date.day, 15)

        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=LDAO_SWS):
            now = datetime.now()
            date = get_default_date()
            self.assertEquals(date.year, now.year)
            self.assertEquals(date.month, now.month)
            self.assertEquals(date.day, now.day)

    def test_is_using_file_dao(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertTrue(is_using_file_dao())

        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=LDAO_SWS):
            self.assertFalse(is_using_file_dao())

    def test_comparison_date(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            no_override = get_comparison_date(now_request)
            self.assertEquals(no_override.year, 2013)
            self.assertEquals(no_override.month, 4)
            self.assertEquals(no_override.day, 15)

            now_request.session["myuw_override_date"] = "2014-01-01"
            no_override = get_comparison_date(now_request)
            self.assertEquals(no_override.year, 2014)
            self.assertEquals(no_override.month, 1)
            self.assertEquals(no_override.day, 1)

    def test_current_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}

            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request.session["myuw_override_date"] = "2013-04-01"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request.session["myuw_override_date"] = "2013-03-25"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'winter')

            now_request.session["myuw_override_date"] = "2013-03-26"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'winter')

            now_request.session["myuw_override_date"] = "2013-03-27"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request.session["myuw_override_date"] = "2013-03-31"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request.session["myuw_override_date"] = "2013-06-24"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            # Spring's grade submission deadline is today, so we're not after
            # that, which is why this is an exception to the rule
            now_request.session["myuw_override_date"] = "2013-06-23"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request.session["myuw_override_date"] = "2013-06-18"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

    def test_next_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}

            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request.session["myuw_override_date"] = "2013-04-01"
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request.session["myuw_override_date"] = "2013-03-31"
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request.session["myuw_override_date"] = "2013-06-24"
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

            now_request.session["myuw_override_date"] = "2013-06-23"
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

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

    def test_get_term_by_year_and_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            quarter = _get_term_by_year_and_quarter(2013, 'spring')
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')
            quarter = _get_term_by_year_and_quarter(2013, 'autumn')
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

    def test_is_past(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            quarter = get_quarter(2013, 'autumn')
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2014-01-01"
            self.assertTrue(is_past(quarter, now_request))

    def test_is_summer_term(self):
            self.assertTrue(is_a_term('A-term'))
            self.assertTrue(is_b_term('B-term'))
            self.assertTrue(is_half_summer_term('A-term'))
            self.assertTrue(is_half_summer_term('B-term'))
            self.assertFalse(is_half_summer_term('Full-term'))
            self.assertTrue(is_full_summer_term('Full-term'))
            self.assertTrue(is_same_summer_term('A-term', 'a-term'))
            self.assertFalse(is_same_summer_term('A-term', 'Full-term'))

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

    def test_is_current_summer_a_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-10"
            self.assertTrue(is_current_summer_a_term(now_request))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-10"
            self.assertFalse(is_current_summer_a_term(now_request))
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-10"
            self.assertFalse(is_current_summer_a_term(now_request))

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
