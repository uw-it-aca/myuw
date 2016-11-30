from datetime import datetime
from django.test import TestCase
from django.conf import settings
from restclients.models.sws import ClassSchedule, Term, Section, Person
from myuw.dao.term import get_specific_term, is_past,\
    get_default_date, get_comparison_date,\
    get_current_quarter, get_next_quarter, is_past,\
    get_next_non_summer_quarter, get_next_autumn_quarter,\
    is_in_summer_a_term, is_in_summer_b_term,\
    get_bod_current_term_class_start, get_eod_7d_after_class_start,\
    get_eod_current_term, get_eod_current_term_last_instruction,\
    get_bod_7d_before_last_instruction, get_eod_current_term_last_final_exam,\
    get_bod_class_start_quarter_after, get_eod_specific_quarter,\
    get_eod_specific_quarter_after, get_eod_specific_quarter_last_instruction
from myuw.test import FDAO_SWS, LDAO_SWS, FDAO_PWS, get_request_with_date,\
    get_request_with_user


class TestTerm(TestCase):
    def setUp(self):
        get_request_with_user('javerage')

    def test_get_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date(None)
            term = get_specific_term(2013, "summer")
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, "summer")
            self.assertFalse(is_past(term, now_request))

    def test_is_past_1(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date(None)
            term = get_specific_term(2014, "winter")
            self.assertEqual(term.year, 2014)
            self.assertEqual(term.quarter, "winter")
            self.assertFalse(is_past(term, now_request))

            term = get_specific_term(2013, "winter")
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, "winter")
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

    def test_comparison_date(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date(None)
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
            now_request = get_request_with_date(None)

            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request = get_request_with_date("2013-04-01")
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request = get_request_with_date("2013-03-25")
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'winter')

            now_request = get_request_with_date("2013-03-26")
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'winter')

            now_request = get_request_with_date("2013-03-27")
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request = get_request_with_date("2013-03-31")
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request = get_request_with_date("2013-06-24")
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            # Spring's grade submission deadline is today, so we're not after
            # that, which is why this is an exception to the rule
            now_request = get_request_with_date("2013-06-23")
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request = get_request_with_date("2013-06-18")
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

    def test_next_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date(None)
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request = get_request_with_date("2013-04-01")
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request = get_request_with_date("2013-03-31")
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request = get_request_with_date("2013-06-24")
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

            now_request = get_request_with_date("2013-06-23")
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

    def test_is_past_2(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            quarter = get_specific_term(2013, 'autumn')
            now_request = get_request_with_date("2014-01-01")
            self.assertTrue(is_past(quarter, now_request))

    def test_get_next_non_summer_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-04-01")
            quarter = get_next_non_summer_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

    def test_get_next_autumn_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-04-01")
            quarter = get_next_autumn_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

    def test_is_in_summer_a_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-07-10")
            self.assertTrue(is_in_summer_a_term(now_request))
            now_request = get_request_with_date("2013-08-10")
            self.assertFalse(is_in_summer_a_term(now_request))
            now_request = get_request_with_date("2013-08-26")
            self.assertTrue(is_in_summer_b_term(now_request))
            now_request = get_request_with_date("2013-03-10")
            self.assertFalse(is_in_summer_a_term(now_request))
            now_request = get_request_with_date("2013-03-10")
            self.assertFalse(is_in_summer_b_term(now_request))

    def test_get_eod_current_term_last_instruction(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-05-10")
            self.assertEqual(
                get_eod_current_term_last_instruction(now_request),
                datetime(2013, 6, 8, 0, 0, 0))
            now_request = get_request_with_date("2013-07-10")
            self.assertEqual(
                get_eod_current_term_last_instruction(now_request, True),
                datetime(2013, 7, 25, 0, 0, 0))
            now_request = get_request_with_date("2013-07-10")
            self.assertEqual(
                get_eod_current_term_last_instruction(now_request),
                datetime(2013, 8, 24, 0, 0, 0))
            now_request = get_request_with_date("2013-08-10")
            self.assertEqual(
                get_eod_current_term_last_instruction(now_request, True),
                datetime(2013, 8, 24, 0, 0, 0))

    def test_get_bod_7d_before_last_instruction(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-05-10")
            self.assertEqual(get_bod_7d_before_last_instruction(now_request),
                             datetime(2013, 5, 31, 0, 0, 0))
            now_request = get_request_with_date("2013-07-10")
            self.assertEqual(get_bod_7d_before_last_instruction(now_request),
                             datetime(2013, 7, 17, 0, 0, 0))
            now_request = get_request_with_date("2013-08-10")
            self.assertEqual(get_bod_7d_before_last_instruction(now_request),
                             datetime(2013, 8, 16, 0, 0, 0))

    def test_get_bod_current_term_class_start(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-05-10")
            self.assertEqual(get_bod_current_term_class_start(now_request),
                             datetime(2013, 4, 1, 0, 0, 0))
            now_request = get_request_with_date("2013-07-10")
            self.assertEqual(get_bod_current_term_class_start(now_request),
                             datetime(2013, 6, 24, 0, 0, 0))
            now_request = get_request_with_date("2013-08-10")
            self.assertEqual(get_bod_current_term_class_start(now_request),
                             datetime(2013, 6, 24, 0, 0, 0))

    def test_get_eod_7d_after_class_start(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-05-10")
            self.assertEqual(get_eod_7d_after_class_start(now_request),
                             datetime(2013, 4, 9, 0, 0, 0))
            now_request = get_request_with_date("2013-07-10")
            self.assertEqual(get_eod_7d_after_class_start(now_request),
                             datetime(2013, 7, 2, 0, 0, 0))
            now_request = get_request_with_date("2013-08-10")
            self.assertEqual(get_eod_7d_after_class_start(now_request),
                             datetime(2013, 7, 2, 0, 0, 0))

    def test_get_bod_class_start_quarter_after(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            quarter = get_specific_term(2013, 'winter')
            self.assertEqual(get_bod_class_start_quarter_after(quarter),
                             datetime(2013, 4, 1, 0, 0, 0))
            quarter = get_specific_term(2013, 'spring')
            self.assertEqual(get_bod_class_start_quarter_after(quarter),
                             datetime(2013, 6, 24, 0, 0, 0))
            quarter = get_specific_term(2013, 'summer')
            self.assertEqual(get_bod_class_start_quarter_after(quarter),
                             datetime(2013, 9, 25, 0, 0, 0))

    def test_get_eod_current_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-03-10")
            self.assertEqual(get_eod_current_term(now_request),
                             datetime(2013, 3, 27, 0, 0, 0))
            now_request = get_request_with_date("2013-07-10")
            self.assertEqual(get_eod_current_term(now_request, True),
                             datetime(2013, 7, 25, 0, 0, 0))
            now_request = get_request_with_date("2013-08-10")
            self.assertEqual(get_eod_current_term(now_request),
                             datetime(2013, 8, 28, 0, 0, 0))

    def test_get_eod_current_term_last_final_exam(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            now_request = get_request_with_date("2013-03-10")
            self.assertEqual(
                get_eod_current_term_last_final_exam(now_request),
                datetime(2013, 3, 23, 0, 0, 0))
            now_request = get_request_with_date("2013-07-10")
            self.assertEqual(
                get_eod_current_term_last_final_exam(now_request, True),
                datetime(2013, 7, 25, 0, 0, 0))
            now_request = get_request_with_date("2013-08-10")
            self.assertEqual(
                get_eod_current_term_last_final_exam(now_request),
                datetime(2013, 8, 24, 0, 0, 0))

    def test_get_eod_specific_quarter_last_instruction(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertEqual(
                get_eod_specific_quarter_last_instruction(2013, "spring"),
                datetime(2013, 6, 8, 0, 0, 0))
            self.assertEqual(
                get_eod_specific_quarter_last_instruction(2013, "summer"),
                datetime(2013, 8, 24, 0, 0, 0))

    def test_get_eod_specific_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertEqual(get_eod_specific_quarter(2013, "autumn"),
                             datetime(2013, 12, 18, 0, 0, 0))
            self.assertEqual(get_eod_specific_quarter(2013, "summer"),
                             datetime(2013, 8, 28, 0, 0, 0))

    def test_get_eod_specific_quarter_after(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertEqual(get_eod_specific_quarter_after(2013, "summer"),
                             datetime(2013, 12, 18, 0, 0, 0))
            self.assertEqual(get_eod_specific_quarter_after(2013, "spring"),
                             datetime(2013, 8, 28, 0, 0, 0))
