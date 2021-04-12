# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf
from django.test.utils import override_settings
from django.urls import reverse
from myuw.util.settings import get_logout_url
from myuw.test.api import missing_url, MyuwApiTest
from myuw.test.views import get_desktop_args


class TestLogoutLink(MyuwApiTest):

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_logout(self):
        logout_url = reverse("myuw_logout")
        home_url = reverse("myuw_home")
        self.set_user('javerage')
        old_session_id = self.client.cookies['sessionid'].value
        response = self.client.get(logout_url, **get_desktop_args())
        new_session_id = self.client.cookies['sessionid'].value
        self.assertNotEqual(old_session_id, new_session_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], get_logout_url())
