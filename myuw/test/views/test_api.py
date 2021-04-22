# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from unittest import skipIf
from django.urls import reverse
from myuw.views.api import OpenAPI
from myuw.test.api import missing_url, MyuwApiTest
from datetime import datetime


class TestDispatchErrorCases(MyuwApiTest):

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage(self):
        url = reverse("myuw_book_api",
                      kwargs={'year': 2013,
                              'quarter': 'spring',
                              'summer_term': ''})
        self.set_user('javerage')
        response = self.client.put(url)
        self.assertEquals(response.status_code, 405)

        response = self.client.post(url)
        self.assertEquals(response.status_code, 405)

        response = self.client.delete(url)
        self.assertEquals(response.status_code, 405)


class TestJSONResponse(MyuwApiTest):
    def test_json_response(self):
        response = OpenAPI().json_response(None)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), None)

        response = OpenAPI().json_response('', status=403)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(json.loads(response.content), '')

        response = OpenAPI().json_response(datetime(2013, 1, 1, 0, 0, 0))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content), '2013-01-01 00:00:00')
