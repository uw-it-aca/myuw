from django.test import TestCase
from myuw.dao.class_website import _fetch_url


class TestClassWebsiteDao(TestCase):

    def test_fetch_live_url(self):
        with self.settings(RESTCLIENTS_WWW_DAO_CLASS='Live'):
            self.assertIsNotNone(_fetch_url(
                    "http://www.washington.edu/classroom/DEM+012"))

    def test_fetch_mock_url(self):
        with self.settings(RESTCLIENTS_WWW_DAO_CLASS='Mock'):
            self.assertIsNotNone(_fetch_url(
                    "http://www.washington.edu/classroom/SMI+401"))
