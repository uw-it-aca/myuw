# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import reverse
from django.test.utils import override_settings
from myuw.test import get_request_with_user
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_home')
class TestLogins(MyuwApiTest):

    _mobile_args = {
        'HTTP_USER_AGENT': ("Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 "
                            "like Mac OS X) AppleWebKit/536.26 (KHTML, "
                            "like Gecko) Version/6.0 Mobile/10B329 "
                            "Safari/8536.25")}

    _desktop_args = {
        'HTTP_USER_AGENT': ("Mozilla/5.0 (compatible; MSIE 10.0; Windows "
                            "NT 6.2; ARM; Trident/6.0; Touch)")}

    def get_home_desktop(self):
        return self.client.get(reverse('myuw_home'), **self._desktop_args)

    def get_home_mobile(self):
        return self.client.get(reverse('myuw_home'), **self._mobile_args)

    def test_mobile_login(self):
        self.set_user('jnew')
        response = self.get_home_mobile()
        self.assertEquals(response.status_code, 200)

        self.set_user('japplicant')
        response = self.get_home_mobile()
        self.assertEquals(response.status_code, 200)

        self.set_user('curgrad')
        response = self.get_home_mobile()
        self.assertEquals(response.status_code, 200)

    def test_desktop_login(self):
        self.set_user('none')
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)

        self.set_user("jbothell")
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)

        self.set_user("faculty")
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)

        self.set_user('staff')
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)
