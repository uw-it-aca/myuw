from django.test import TestCase
from django.conf import settings
from myuw.util.settings import get_calendar_time_zone,\
    get_mailman_courserequest_recipient, get_google_search_key,\
    get_legacy_url, get_logout_url, get_myuwclass_url


class TestSetting(TestCase):

    def test_default(self):
        self.assertEqual(get_calendar_time_zone(), 'America/Los_Angeles')
        self.assertIsNone(get_mailman_courserequest_recipient())
        self.assertIsNone(get_google_search_key())
        self.assertEqual(get_legacy_url(),
                         "https://myuw.washington.edu/servlet/user")
        self.assertEqual(get_logout_url(), "/user_logout")
        self.assertEqual(get_myuwclass_url(), "myuwclass.asp?cid=")
