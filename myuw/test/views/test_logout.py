# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf

from django.urls import reverse

from myuw.test.api import MyuwApiTest, missing_url
from myuw.test.views import get_desktop_args
from myuw.util.settings import get_logout_url


class TestLogoutLink(MyuwApiTest):

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_logout(self):
        logout_url = reverse("myuw_logout")
        self.set_user('javerage')
        old_session_id = self.client.cookies['sessionid'].value
        response = self.client.get(logout_url, **get_desktop_args())
        new_session_id = self.client.cookies['sessionid'].value
        self.assertNotEqual(old_session_id, new_session_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], get_logout_url())
