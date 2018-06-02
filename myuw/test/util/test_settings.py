from django.test import TestCase
from django.conf import settings
from myuw.util.settings import get_calendar_time_zone,\
    get_mailman_courserequest_recipient, get_google_search_key,\
    get_legacy_url, get_logout_url, get_myuwclass_url


legacy_url = "https://myuw.washington.edu/"


class TestSetting(TestCase):

    def test_default(self):
        with self.settings(TRUMBA_CALENDAR_TIMEZONE='America/Los_Angeles',
                           MAILMAN_COURSEREQUEST_RECIPIENT="",
                           GOOGLE_SEARCH_KEY="",
                           MYUW_USER_SERVLET_URL=legacy_url,
                           LOGOUT_URL="/user_logout",
                           MYUWCLASS="myuwclass.asp?cid="):
            self.assertEqual(get_calendar_time_zone(), 'America/Los_Angeles')
            self.assertEqual(get_mailman_courserequest_recipient(), "")
            self.assertEqual(get_google_search_key(), "")
            self.assertEqual(get_legacy_url(), legacy_url)
            self.assertEqual(get_logout_url(), "/user_logout")
            self.assertEqual(get_myuwclass_url(), "myuwclass.asp?cid=")
