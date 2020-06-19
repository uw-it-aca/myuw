import re
from django.test import TestCase
from django.conf import settings
from myuw.util.settings import (
    get_calendar_time_zone, get_myuwclass_url, get_myuw_test_access_group,
    get_mailman_courserequest_recipient, get_google_search_key,
    get_myuw_admin_group, get_myuw_override_group, get_myuw_astra_group_stem,
    get_disable_actions_when_override, get_enabled_features, get_logout_url,
    no_access_check, get_cronjob_recipient, get_cronjob_sender)


class TestSetting(TestCase):

    def test_default(self):
        with self.settings(TRUMBA_CALENDAR_TIMEZONE='America/Los_Angeles',
                           MAILMAN_COURSEREQUEST_RECIPIENT="",
                           GOOGLE_SEARCH_KEY="",
                           LOGOUT_URL="/user_logout",
                           MYUW_SKIP_ACCESS_CHECK=False,
                           MYUWCLASS="myuwclass.asp?cid=",
                           MYUW_ADMIN_GROUP='admin',
                           MYUW_OVERRIDE_GROUP='impersonate',
                           MYUW_ASTRA_GROUP_STEM='u_astratst_myuw',
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True,
                           MYUW_TEST_ACCESS_GROUP='u_dev_test-access',
                           MYUW_ENABLED_FEATURES=[],
                           CRONJOB_RECIPIENT="mycron",
                           CRONJOB_SENDER="my"):

            self.assertEqual(get_calendar_time_zone(), 'America/Los_Angeles')
            self.assertEqual(get_mailman_courserequest_recipient(), "")
            self.assertEqual(get_google_search_key(), "")
            self.assertEqual(get_logout_url(), "/user_logout")
            self.assertFalse(no_access_check())
            self.assertEqual(get_myuwclass_url(), "myuwclass.asp?cid=")
            self.assertEqual(get_myuw_admin_group(), 'admin')
            self.assertEqual(get_myuw_override_group(), 'impersonate')
            self.assertEqual(get_myuw_astra_group_stem(), 'u_astratst_myuw')
            self.assertEqual(get_myuw_test_access_group(), 'u_dev_test-access')
            self.assertEqual(get_disable_actions_when_override(), True)
            self.assertEqual(get_enabled_features(), [])
            self.assertEqual(get_cronjob_recipient(), "mycron")
            self.assertEqual(get_cronjob_sender(), "my")
