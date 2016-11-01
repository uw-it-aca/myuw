from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from django.test.utils import override_settings
from userservice.user import UserServiceMiddleware
from datetime import datetime
from myuw.dao.term import get_default_date, get_comparison_datetime,\
    get_specific_term
from myuw.dao.card_display_dates import get_card_visibilty_date_values,\
    in_show_grades_period, is_before_bof_term,\
    is_before_eof_7d_after_class_start,\
    is_after_7d_before_last_instruction, is_before_last_day_of_classes,\
    is_after_last_day_of_classes, is_before_eof_finals_week, \
    is_after_bof_and_before_eof_reg_period,\
    is_after_bof_and_before_eof_summer_reg_period1,\
    is_after_bof_and_before_eof_summer_reg_periodA,\
    during_myplan_peak_load

FDAO_SWS = 'restclients.dao_implementation.sws.File'


@override_settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS)
class TestDisplayValues(TestCase):

    def get_request_for_date(self, date):
        now_request = RequestFactory().get('/')
        now_request.session = {
            'myuw_override_date': date
        }
        UserServiceMiddleware().process_request(now_request)
        return now_request

    def get_visibility_for_date(self, date):
        now_request = self.get_request_for_date(date)
        values = get_card_visibilty_date_values(now_request)
        return values

    def test_first_day(self):
        # spring, before grade submission
        values = self.get_visibility_for_date('2013-03-26')
        self.assertTrue(values["is_after_last_day_of_classes"])
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_before_first_day_of_term"])
        # spring, after grade submission
        now_request = self.get_request_for_date('2013-03-27')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(values["is_after_grade_submission_deadline"])
        self.assertTrue(values["is_before_first_day_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(is_before_bof_term(now, now_request))
        # spring, before instruction begins
        now_request = self.get_request_for_date('2013-03-31')
        values = get_card_visibilty_date_values(now_request)
        self.assertTrue(values["is_before_first_day_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(is_before_bof_term(now, now_request))

        # spring, instruction begins
        now_request = self.get_request_for_date('2013-04-01')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertFalse(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertFalse(
            values["is_before_end_of_registration_display_period"])
        self.assertFalse(values["is_before_first_day_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertFalse(is_before_bof_term(now, now_request))

        # autumn
        values = self.get_visibility_for_date('2012-08-21')
        self.assertTrue(values["is_after_last_day_of_classes"])
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_before_first_day_of_term"])

        values = self.get_visibility_for_date('2012-08-22')
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(values["is_after_grade_submission_deadline"])
        self.assertTrue(values["is_before_first_day_of_term"])

        values = self.get_visibility_for_date('2012-09-24')
        self.assertFalse(values["is_before_first_day_of_term"])

        values = self.get_visibility_for_date('2012-09-23')
        self.assertTrue(values["is_before_first_day_of_term"])

        # winter
        values = self.get_visibility_for_date('2013-12-17')
        self.assertTrue(values["is_after_last_day_of_classes"])
        self.assertFalse(values["is_after_grade_submission_deadline"])

        values = self.get_visibility_for_date('2013-12-18')
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(values["is_after_grade_submission_deadline"])

        values = self.get_visibility_for_date('2013-01-07')
        self.assertFalse(values["is_before_first_day_of_term"])

        values = self.get_visibility_for_date('2013-01-06')
        self.assertTrue(values["is_before_first_day_of_term"])

        # summer
        values = self.get_visibility_for_date('2012-06-12')
        self.assertTrue(values["is_after_last_day_of_classes"])
        self.assertFalse(values["is_after_grade_submission_deadline"])

        values = self.get_visibility_for_date('2012-06-13')
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(values["is_after_grade_submission_deadline"])

        values = self.get_visibility_for_date('2012-06-18')
        self.assertFalse(values["is_before_first_day_of_term"])

        values = self.get_visibility_for_date('2012-06-17')
        self.assertTrue(values["is_before_first_day_of_term"])

    def test_is_before_eof_7days_of_term(self):
        values = self.get_visibility_for_date('2013-03-26')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_before_eof_7days_of_term"])
        # spring
        values = self.get_visibility_for_date('2013-03-27')
        self.assertTrue(values["is_before_eof_7days_of_term"])

        now_request = self.get_request_for_date('2013-04-08')
        values = get_card_visibilty_date_values(now_request)
        self.assertTrue(values["is_before_eof_7days_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(
            is_before_eof_7d_after_class_start(now, now_request))

        now_request = self.get_request_for_date('2013-04-09')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_before_eof_7days_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertFalse(
            is_before_eof_7d_after_class_start(now, now_request))

        now_request = self.get_request_for_date('2012-08-21')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_after_grade_submission_deadline"])

        # autumn
        values = self.get_visibility_for_date('2012-08-22')
        self.assertTrue(values["is_before_eof_7days_of_term"])

        now_request = self.get_request_for_date('2012-10-01')
        values = get_card_visibilty_date_values(now_request)
        self.assertTrue(values["is_before_eof_7days_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(
            is_before_eof_7d_after_class_start(now, now_request))

        now_request = self.get_request_for_date('2012-10-02')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_before_eof_7days_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertFalse(
            is_before_eof_7d_after_class_start(now, now_request))

        values = self.get_visibility_for_date('2012-12-18')
        self.assertFalse(values["is_after_grade_submission_deadline"])

        # winter
        values = self.get_visibility_for_date('2012-12-19')
        self.assertTrue(values["is_before_eof_7days_of_term"])

        now_request = self.get_request_for_date('2013-01-14')
        values = get_card_visibilty_date_values(now_request)
        self.assertTrue(values["is_before_eof_7days_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(
            is_before_eof_7d_after_class_start(now, now_request))

        now_request = self.get_request_for_date('2013-01-15')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_before_eof_7days_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertFalse(
            is_before_eof_7d_after_class_start(now, now_request))

        values = self.get_visibility_for_date('2012-06-12')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        # summer
        values = self.get_visibility_for_date('2012-06-13')
        self.assertTrue(values["is_before_eof_7days_of_term"])

        now_request = self.get_request_for_date('2012-06-25')
        values = get_card_visibilty_date_values(now_request)
        self.assertTrue(values["is_before_eof_7days_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(
            is_before_eof_7d_after_class_start(now, now_request))

        # A-term, Full-term
        now_request = self.get_request_for_date('2012-06-26')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_before_eof_7days_of_term"])
        now = get_comparison_datetime(now_request)
        self.assertFalse(
            is_before_eof_7d_after_class_start(now, now_request))

        # B-term
        now_request = self.get_request_for_date('2012-07-26')
        values = get_card_visibilty_date_values(now_request)
        now = get_comparison_datetime(now_request)
        self.assertFalse(
            is_before_eof_7d_after_class_start(now, now_request))

    def test_is_after_7d_before_last_instruction(self):
        # spring
        values = self.get_visibility_for_date('2013-05-30')
        self.assertFalse(values["is_after_7d_before_last_instruction"])

        values = self.get_visibility_for_date('2013-05-31')
        self.assertTrue(values["is_after_7d_before_last_instruction"])

        values = self.get_visibility_for_date('2013-06-24')
        self.assertFalse(values["is_after_7d_before_last_instruction"])

        # summer a-term
        values = self.get_visibility_for_date('2012-07-10')
        self.assertFalse(values["is_after_7d_before_last_instruction"])

        values = self.get_visibility_for_date('2012-07-11')
        self.assertTrue(values["is_after_7d_before_last_instruction"])

        # b-term start
        values = self.get_visibility_for_date('2012-07-19')
        self.assertFalse(values["is_after_7d_before_last_instruction"])

        # summer b-term or full-term
        values = self.get_visibility_for_date('2012-08-09')
        self.assertFalse(values["is_after_7d_before_last_instruction"])

        values = self.get_visibility_for_date('2012-08-10')
        self.assertTrue(values["is_after_7d_before_last_instruction"])

        values = self.get_visibility_for_date('2012-08-22')
        self.assertFalse(values["is_after_7d_before_last_instruction"])

    def test_day_before_last_day_of_classes(self):

        now_request = self.get_request_for_date('2013-06-06')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertTrue(
            values["is_before_end_of_registration_display_period"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(is_before_last_day_of_classes(now, now_request))
        self.assertTrue(
            is_after_bof_and_before_eof_reg_period(now, now_request))

        # winter
        now_request = self.get_request_for_date('2013-03-14')
        now = get_comparison_datetime(now_request)
        self.assertTrue(
            is_before_last_day_of_classes(now, now_request))
        self.assertFalse(
            is_after_last_day_of_classes(now, now_request))

    def test_day_on_last_day_of_classes(self):
        now_request = self.get_request_for_date('2013-06-07')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertTrue(
            values["is_before_end_of_registration_display_period"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(
            is_before_last_day_of_classes(now, now_request))
        self.assertFalse(
            is_after_last_day_of_classes(now, now_request))
        self.assertTrue(
            is_after_bof_and_before_eof_reg_period(now, now_request))

    def test_day_after_last_day_of_classes(self):
        values = self.get_visibility_for_date('2013-06-08')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertTrue(values["is_after_last_day_of_classes"])
        self.assertTrue(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertFalse(values["is_before_last_day_of_classes"])
        self.assertTrue(
            values["is_before_end_of_registration_display_period"])

        # 2013 winter after
        now_request = self.get_request_for_date('2013-03-16')
        now = get_comparison_datetime(now_request)
        self.assertTrue(
            is_after_last_day_of_classes(now, now_request))
        self.assertFalse(
            is_before_last_day_of_classes(now, now_request))

    def test_last_final_exam_day(self):
        # spring
        now_request = self.get_request_for_date('2013-06-14')
        values = get_card_visibilty_date_values(now_request)
        self.assertTrue(values["is_after_last_day_of_classes"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        now = get_comparison_datetime(now_request)
        self.assertTrue(is_before_eof_finals_week(now, now_request))
        self.assertFalse(is_before_last_day_of_classes(now, now_request))

        now_request = self.get_request_for_date('2013-06-15')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_before_end_of_finals_week"])
        self.assertFalse(values["is_before_last_day_of_classes"])
        now = get_comparison_datetime(now_request)
        self.assertFalse(is_before_eof_finals_week(now, now_request))

        # autumn
        values = self.get_visibility_for_date('2013-12-13')
        self.assertTrue(values["is_before_end_of_finals_week"])

        now_request = self.get_request_for_date('2013-12-14')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_before_end_of_finals_week"])
        now = get_comparison_datetime(now_request)
        self.assertFalse(is_before_eof_finals_week(now, now_request))

        # winter
        values = self.get_visibility_for_date('2013-03-22')
        self.assertTrue(values["is_before_end_of_finals_week"])
        now_request = self.get_request_for_date('2013-03-23')
        values = get_card_visibilty_date_values(now_request)
        self.assertFalse(values["is_before_end_of_finals_week"])
        now = get_comparison_datetime(now_request)
        self.assertFalse(is_before_eof_finals_week(now, now_request))

    def test_13_days_before_period1_registration(self):
        # Using winter term dates, because spring/summer dates
        # are too close together
        values = self.get_visibility_for_date('2013-02-02')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertTrue(
            values["is_before_end_of_registration_display_period"])

    def test_14_days_before_period1_registration(self):
        values = self.get_visibility_for_date('2013-02-01')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertTrue(
            values["is_before_end_of_registration_display_period"])

    def test_15_days_before_period1_registration(self):
        values = self.get_visibility_for_date('2013-01-31')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertFalse(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertFalse(
            values["is_before_end_of_registration_display_period"])

    def test_6_days_after_period2_registration(self):
        values = self.get_visibility_for_date('2013-03-10')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertTrue(
            values["is_before_end_of_registration_display_period"])

    def test_7_days_after_period2_registration(self):
        values = self.get_visibility_for_date('2013-03-11')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertFalse(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertFalse(
            values["is_before_end_of_registration_display_period"])

    def test_day_of_grade_submission_deadline(self):
        # We need to test in winter, because spring's grade submission
        # deadline is replaced to test grade submission
        values = self.get_visibility_for_date('2013-03-26')
        self.assertFalse(values["is_after_grade_submission_deadline"])
        self.assertTrue(values["is_after_last_day_of_classes"])
        self.assertFalse(
            values["is_after_start_of_registration_display_period"])
        self.assertFalse(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertFalse(values["is_before_last_day_of_classes"])
        self.assertFalse(
            values["is_before_end_of_registration_display_period"])

    def test_day_after_grade_submission_deadline(self):
        # We need to test in winter, because spring's grade submission
        # deadline is replaced to test grade submission
        values = self.get_visibility_for_date('2013-03-27')
        self.assertTrue(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertTrue(values["is_before_first_day_of_term"])
        self.assertFalse(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        # This is a poorly named value - it's really last day + 1
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertFalse(
            values["is_before_end_of_registration_display_period"])

    def test_js_overrides(self):
        now_request = self.get_request_for_date('2013-04-01')
        # Swapping one true, and one false value
        # from the test_first_day test
        now_request.session["myuw_after_submission"] = True
        now_request.session["myuw_after_reg"] = False

        values = get_card_visibilty_date_values(now_request)
        self.assertTrue(values["is_after_grade_submission_deadline"])
        self.assertFalse(values["is_after_last_day_of_classes"])
        self.assertFalse(
            values["is_after_start_of_registration_display_period"])
        self.assertTrue(values["is_before_end_of_finals_week"])
        self.assertTrue(values["is_before_last_day_of_classes"])
        self.assertFalse(
            values["is_before_end_of_registration_display_period"])

    def test_in_show_grades_period(self):
        term = get_specific_term(2013, "winter")
        now_request = self.get_request_for_date('2013-03-27')
        self.assertTrue(in_show_grades_period(term, now_request))
        # spring quarter starts
        now_request = self.get_request_for_date('2013-04-01')
        self.assertFalse(in_show_grades_period(term, now_request))

    def test_myplan_peak_loads(self):

        # Assert peak load false on these dates
        peak_load_false = (
            '2013-04-14 06:00:00',
            '2013-04-15 05:29:59',
            '2013-06-23 06:30:01',
        )

        # Assert peak load true on these dates
        peak_load_true = (
            '2013-04-15 05:30:00',
            '2013-04-16 06:29:00',
            '2013-05-10 06:29:00',
            '2013-05-10 06:30:00',
            '2013-05-22 06:30:00',
            '2013-05-23 06:29:00',
            '2013-02-15 06:00:00',
            '2013-04-15 06:00:00',
            '2013-05-11 06:00:00',
            '2013-06-23 06:00:00',
        )

        for date in peak_load_false:
            values = self.get_visibility_for_date(date)
            self.assertFalse(
                values['myplan_peak_load'],
                'Expected MyPlan peak load to be False on date %s' % date)

        for date in peak_load_true:
            values = self.get_visibility_for_date(date)
            self.assertTrue(
                values['myplan_peak_load'],
                'Expected MyPlan peak load to be True on date %s' % date)
