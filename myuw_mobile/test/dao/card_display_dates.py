from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from datetime import datetime
from myuw_mobile.dao.term import get_default_date
from myuw_mobile.dao.card_display_dates import get_card_visibilty_date_values


class TestDisplayValues(TestCase):

    def test_first_day(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            # spring
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-26"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_before_first_day_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-27"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_grade_submission_deadline"])
            self.assertTrue(values["is_before_first_day_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-01"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertFalse(values["is_before_end_of_registration_display_period"])
            self.assertFalse(values["is_before_first_day_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-31"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_first_day_of_term"])

            # autumn
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-08-21"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_before_first_day_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-08-22"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_grade_submission_deadline"])
            self.assertTrue(values["is_before_first_day_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-09-24"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_before_first_day_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-09-23"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_first_day_of_term"])

            # winter
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-12-17"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_grade_submission_deadline"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-12-18"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_grade_submission_deadline"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-01-07"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_before_first_day_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-01-06"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_first_day_of_term"])

            # summer
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-06-12"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_grade_submission_deadline"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-06-13"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_grade_submission_deadline"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-06-18"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_before_first_day_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-06-17"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_first_day_of_term"])

    def test_is_before_eof_7days_of_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-26"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_before_eof_7days_of_term"])
            # spring
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-27"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_eof_7days_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-08"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_eof_7days_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-09"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_before_eof_7days_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-08-21"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            # autumn
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-08-22"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_eof_7days_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-10-01"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_eof_7days_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-10-02"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_before_eof_7days_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-12-18"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            # winter
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-12-19"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_eof_7days_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-01-14"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_eof_7days_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-01-15"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_before_eof_7days_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-06-12"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            # summer
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-06-13"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_eof_7days_of_term"])
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-06-25"
            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_before_eof_7days_of_term"])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-06-26"
            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_before_eof_7days_of_term"])

    def test_day_before_last_day_of_classes(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-06"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

    def test_last_day_of_classes(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-07"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

    def test_day_after_last_day_of_classes(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-08"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertTrue(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertFalse(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

    def test_last_final_exam_day(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-14"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertTrue(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertFalse(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertFalse(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

    def test_day_after_last_final_exam_day(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-15"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertTrue(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertFalse(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertFalse(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

    def test_13_days_before_period1_registration(self):
        # Using winter term dates, because spring/summer dates are too close together
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-02-02"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

    def test_14_days_before_period1_registration(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-02-01"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

    def test_15_days_before_period1_registration(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-01-31"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertFalse(values["is_before_end_of_registration_display_period"])

    def test_6_days_after_period2_registration(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-10"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

    def test_7_days_after_period2_registration(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-11"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertFalse(values["is_before_end_of_registration_display_period"])

    def test_day_of_grade_submission_deadline(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            # We need to test in winter, because spring's grade submission
            # deadline is replaced to test grade submission
            now_request.session["myuw_override_date"] = "2013-03-26"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertTrue(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_start_of_registration_display_period"])
            self.assertFalse(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertFalse(values["is_before_last_day_of_classes"])
            self.assertFalse(values["is_before_end_of_registration_display_period"])

    def test_day_after_grade_submission_deadline(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            # We need to test in winter, because spring's grade submission
            # deadline is replaced to test grade submission
            now_request.session["myuw_override_date"] = "2013-03-27"

            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_before_first_day_of_term"])
            self.assertFalse(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertFalse(values["is_before_end_of_registration_display_period"])

    def test_js_overrides(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-01"

            # Swapping one true, and one false value from the test_first_day test
            now_request.session["myuw_after_submission"] = True
            now_request.session["myuw_after_reg"] = False

            values = get_card_visibilty_date_values(now_request)
            self.assertTrue(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertFalse(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertFalse(values["is_before_end_of_registration_display_period"])
