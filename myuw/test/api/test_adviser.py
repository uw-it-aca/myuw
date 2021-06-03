# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, require_url, fdao_sws_override


@fdao_sws_override
@require_url('myuw_advisers_api')
class TestAdvisersApi(MyuwApiTest):

    def get_advisers_api_response(self):
        return self.get_response_by_reverse('myuw_advisers_api')

    def test_javerage(self):
        self.set_user('javerage')
        response = self.get_advisers_api_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(
            data[0]["email_address"], "javg001@uw.edu")
        self.assertEquals(
            data[1]["email_address"], "javg002@uw.edu")
        self.assertEquals(
            data[2]["email_address"], "uwhonors@uw.edu")

    def test_errors(self):
        self.set_user('jinter')
        response = self.get_advisers_api_response()
        self.assertEquals(response.status_code, 404)

        self.set_user('jerror')
        response = self.get_advisers_api_response()
        self.assertEquals(response.status_code, 543)
