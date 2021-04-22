# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf
from django.urls import reverse
from myuw.test.api import missing_url, MyuwApiTest


class TestAcademicsMethods(MyuwApiTest):

    @skipIf(missing_url("myuw_thrive_page"), "myuw urls not configured")
    def test_student_access(self):
        url = reverse("myuw_thrive_page")
        self.set_user('javerage')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEquals(response.status_code, 200)
