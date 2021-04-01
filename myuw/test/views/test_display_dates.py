# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf
from django.urls import reverse
from django.test import Client
from myuw.views.display_dates import override
from myuw.test.api import missing_url, require_url, MyuwApiTest


@require_url('myuw_date_override')
class TestViewsLinkAdmin(MyuwApiTest):

    @skipIf(missing_url("myuw_date_override"),
            "myuw_date_override urls not configured")
    def test_admin(self):
        self.set_user('bill')
        url = reverse("myuw_date_override")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_date_override"),
            "myuw_date_override urls not configured")
    def test_override(self):
        self.set_user('faculty')
        url = reverse("myuw_date_override")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    @skipIf(missing_url("myuw_date_override"),
            "myuw_date_override urls not configured")
    def test_override_required_decorator(self):
        self.set_user('none')
        url = reverse("myuw_date_override")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)
