from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory

from myuw_mobile.dao.term import get_default_date
from myuw_mobile.dao.card_display_dates import get_card_visibilty_date_values

from datetime import datetime

class TestDisplayValues(TestCase):
    def test_first_day(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-01"

            values = get_card_visibilty_date_values(now_request)
            self.assertFalse(values["is_after_grade_submission_deadline"])
            self.assertFalse(values["is_after_last_day_of_classes"])
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertTrue(values["is_before_end_of_registration_display_period"])

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
            self.assertFalse(values["is_before_end_of_registration_display_period"])

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
            self.assertFalse(values["is_before_end_of_registration_display_period"])

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
            self.assertFalse(values["is_before_end_of_registration_display_period"])

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
            self.assertFalse(values["is_before_end_of_registration_display_period"])

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
            self.assertFalse(values["is_before_end_of_registration_display_period"])

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
            self.assertTrue(values["is_before_end_of_registration_display_period"])

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
            self.assertTrue(values["is_after_start_of_registration_display_period"])
            self.assertTrue(values["is_before_end_of_finals_week"])
            # This is a poorly named value - it's really last day + 1
            self.assertTrue(values["is_before_last_day_of_classes"])
            self.assertFalse(values["is_before_end_of_registration_display_period"])
