# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from django.test import TestCase
from commonconf import override_settings
from uw_sws.models import ClassSchedule, Term, Section, Person
from myuw.dao.term import (
    get_specific_term, is_past, is_future, sws_now,
    get_default_date, get_default_datetime, get_comparison_date,
    get_current_quarter, get_next_quarter,
    get_previous_quarter, get_previous_number_quarters,
    get_future_number_quarters,
    get_next_non_summer_quarter, get_next_autumn_quarter,
    is_in_summer_a_term, is_in_summer_b_term,
    get_bod_current_term_class_start, get_eod_7d_after_class_start,
    get_eod_current_term, get_eod_current_term_last_instruction,
    get_bod_7d_before_last_instruction, get_eod_current_term_last_final_exam,
    get_bod_class_start_quarter_after, get_eod_specific_quarter,
    get_eod_specific_quarter_after, get_eod_specific_quarter_last_instruction,
    get_current_and_next_quarters, add_term_data_to_context)
from myuw.test import (
    get_request_with_date, get_request_with_user,
    get_request, fdao_sws_override)


ldao_sws_override = override_settings(RESTCLIENTS_SWS_DAO_CLASS='Live')


@fdao_sws_override
class TestTerm(TestCase):
    def setUp(self):
        get_request()

    def test_get_term(self):
        term = get_specific_term(2013, "summer")
        self.assertEqual(term.year, 2013)
        self.assertEqual(term.quarter, "summer")
        self.assertFalse(is_past(term, get_request()))

    def test_is_past_1(self):
        now_request = get_request()
        term = get_specific_term(2014, "winter")
        self.assertEqual(term.year, 2014)
        self.assertEqual(term.quarter, "winter")
        self.assertFalse(is_past(term, now_request))

        term = get_specific_term(2013, "winter")
        self.assertEqual(term.year, 2013)
        self.assertEqual(term.quarter, "winter")
        self.assertTrue(is_past(term, now_request))

    def test_is_future(self):
        term = get_specific_term(2013, "summer")
        now_request = get_request_with_date("2013-04-15")
        self.assertTrue(is_future(term, now_request))

    def test_default_date(self):
        date = get_default_date()
        self.assertEquals(date.year, 2013)
        self.assertEquals(date.month, 4)
        self.assertEquals(date.day, 15)

    @ldao_sws_override
    def test_live_default_date(self):
        now = sws_now()
        date = get_default_datetime()
        self.assertEquals(date.year, now.year)
        self.assertEquals(date.month, now.month)
        self.assertEquals(date.day, now.day)
        self.assertEquals(date.hour, now.hour)

    def test_comparison_date(self):
        now_request = get_request()
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
        now_request = get_request()
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
        now_request = get_request()
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

    def test_get_previous_number_quarters(self):
        now_request = get_request_with_date("2014-01-10")
        quarters = get_previous_number_quarters(now_request, 3)
        self.assertEquals(len(quarters), 3)
        self.assertEquals(quarters[0].year, 2013)
        self.assertEquals(quarters[0].quarter, 'spring')
        self.assertEquals(quarters[1].year, 2013)
        self.assertEquals(quarters[1].quarter, 'summer')
        self.assertEquals(quarters[2].year, 2013)
        self.assertEquals(quarters[2].quarter, 'autumn')

        now_request = get_request_with_date("2013-10-04")
        quarters = get_previous_number_quarters(now_request, 2)
        self.assertEquals(quarters[0].year, 2013)
        self.assertEquals(quarters[0].quarter, 'spring')
        self.assertEquals(quarters[1].year, 2013)
        self.assertEquals(quarters[1].quarter, 'summer')

    def test_get_future_number_quarters(self):
        now_request = get_request_with_date("2013-04-10")
        quarters = get_future_number_quarters(now_request, 1)
        self.assertEquals(quarters[0].year, 2013)
        self.assertEquals(quarters[0].quarter, 'summer')

    def test_is_past_2(self):
        quarter = get_specific_term(2013, 'autumn')
        now_request = get_request_with_date("2014-01-01")
        self.assertTrue(is_past(quarter, now_request))

    def test_get_next_non_summer_quarter(self):
        now_request = get_request_with_date("2013-04-01")
        quarter = get_next_non_summer_quarter(now_request)
        self.assertEquals(quarter.year, 2013)
        self.assertEquals(quarter.quarter, 'autumn')

    def test_get_next_autumn_quarter(self):
        now_request = get_request_with_date("2013-04-01")
        quarter = get_next_autumn_quarter(now_request)
        self.assertEquals(quarter.year, 2013)
        self.assertEquals(quarter.quarter, 'autumn')

    def test_is_in_summer_a_term(self):
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
        self.assertEqual(
            get_eod_specific_quarter_last_instruction(2013, "spring"),
            datetime(2013, 6, 8, 0, 0, 0))
        self.assertEqual(
            get_eod_specific_quarter_last_instruction(2013, "summer"),
            datetime(2013, 8, 24, 0, 0, 0))

    def test_get_eod_specific_quarter(self):
        self.assertEqual(get_eod_specific_quarter(2013, "autumn"),
                         datetime(2013, 12, 18, 0, 0, 0))
        self.assertEqual(get_eod_specific_quarter(2013, "summer"),
                         datetime(2013, 8, 28, 0, 0, 0))

    def test_get_eod_specific_quarter_after(self):
        self.assertEqual(get_eod_specific_quarter_after(2013, "summer"),
                         datetime(2013, 12, 18, 0, 0, 0))
        self.assertEqual(get_eod_specific_quarter_after(2013, "spring"),
                         datetime(2013, 8, 28, 0, 0, 0))

    def test_get_current_and_next_quarters(self):
        date = get_default_date()
        now_request = get_request_with_date(date)
        self.assertEquals(date.year, 2013)
        self.assertEquals(date.month, 4)
        self.assertEquals(date.day, 15)

        quarters = get_current_and_next_quarters(now_request, 4)

        self.assertEqual(len(quarters), 4)

        spring = quarters[0]
        summer = quarters[1]
        autumn = quarters[2]
        winter = quarters[3]

        self.assertEqual(spring.quarter, "spring")
        self.assertEqual(summer.quarter, "summer")
        self.assertEqual(autumn.quarter, "autumn")
        self.assertEqual(winter.quarter, "winter")

        self.assertEqual(spring.year, 2013)
        self.assertEqual(summer.year, 2013)
        self.assertEqual(autumn.year, 2013)
        self.assertEqual(winter.year, 2014)

    def test_term_data_context_in_quarter(self):
        request = get_request_with_date("2013-03-10")

        context = {}
        add_term_data_to_context(request, context)

        self.assertEquals(context['year'], 2013)
        self.assertEquals(context['quarter'], 'winter')
        self.assertEquals(context['is_finals'], False)
        self.assertEquals(context['is_break'], False)

        self.assertEquals(context['today'].year, 2013)
        self.assertEquals(context['today'].month, 3)
        self.assertEquals(context['today'].day, 10)
        self.assertEquals(context['future_term'], "2013,spring")

    def test_term_data_context_in_finals(self):
        request = get_request_with_date("2013-03-22")

        context = {}
        add_term_data_to_context(request, context)
        self.assertEquals(context['year'], 2013)
        self.assertEquals(context['quarter'], 'winter')
        self.assertEquals(context['is_finals'], True)
        self.assertEquals(context['is_break'], False)

    def test_term_data_context_after_finals_break(self):
        request = get_request_with_date("2013-03-23")

        context = {}
        add_term_data_to_context(request, context)
        self.assertEquals(context['year'], 2013)
        self.assertEquals(context['break_year'], 2013)
        self.assertEquals(context['quarter'], 'winter')
        self.assertEquals(context['break_quarter'], 'spring')
        self.assertEquals(context['is_finals'], False)
        self.assertEquals(context['is_break'], True)

    def test_term_dat_context_before_start_break(self):
        request = get_request_with_date("2013-03-29")

        context = {}
        add_term_data_to_context(request, context)
        self.assertEquals(context['year'], 2013)
        self.assertEquals(context['quarter'], 'spring')
        self.assertEquals(context['is_finals'], False)
        self.assertEquals(context['is_break'], True)
