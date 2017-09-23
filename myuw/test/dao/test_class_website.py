from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.class_website import _fetch_url, is_valid_page_url
from myuw.test import get_request


class TestClassWebsiteDao(TestCase):

    def setUp(self):
        get_request()
        # otherwise, UninitializedError: Missing UserServiceMiddleware

    def test_fetch_live_url(self):
        with self.settings(RESTCLIENTS_WWW_DAO_CLASS='Live'):
            response = _fetch_url(
                "http://www.washington.edu/classroom/DEM+012")
            self.assertIsNotNone(response)

            self.assertTrue(
                is_valid_page_url(
                    "http://www.washington.edu/classroom/DEM+012"))

    def test_fetch_mock_url(self):
        with self.settings(RESTCLIENTS_WWW_DAO_CLASS='Mock'):
            response = _fetch_url(
                "http://www.washington.edu/classroom/SMI+401")
            self.assertIsNotNone(response)
            self.assertTrue(
                is_valid_page_url(
                    "http://www.washington.edu/classroom/SMI+401"))

            self.assertRaises(DataFailureException,
                              _fetch_url,
                              "http://www.washington.edu/classroom/DEM+012")
            self.assertFalse(
                is_valid_page_url(
                    "http://www.washington.edu/classroom/DEM+012"))
