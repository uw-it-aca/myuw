# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf

from django.urls import reverse

from myuw.test.api import MyuwApiTest, missing_url, require_url


@require_url('myuw_date_override')
class TestViewsLinkAdmin(MyuwApiTest):

    @skipIf(missing_url("myuw_date_override"),
            "myuw_date_override urls not configured")
    def test_admin(self):
        self.set_user('bill')
        url = reverse("myuw_date_override")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @skipIf(missing_url("myuw_date_override"),
            "myuw_date_override urls not configured")
    def test_override_required_decorator(self):
        self.set_user('none')
        url = reverse("myuw_date_override")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
