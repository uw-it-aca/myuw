# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_attest_covid19')
class TestCovid19AttestationApi(MyuwApiTest):

    def get_covid19_api_response(self):
        return self.get_response_by_reverse('myuw_attest_covid19')

    def test_vaccinated(self):
        self.set_user('javerage')
        response = self.get_covid19_api_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsNotNone(data.get("vaccinated"))
        self.assertIsNone(data.get("exemption"))

    def test_exemption(self):
        self.set_user('jinter')
        response = self.get_covid19_api_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsNone(data.get("vaccinated"))
        self.assertIsNotNone(data.get("exemption"))

    def test_errors(self):
        self.set_user('jalum')
        response = self.get_covid19_api_response()
        self.assertEquals(response.status_code, 404)

        self.set_user('jerror')
        response = self.get_covid19_api_response()
        self.assertEquals(response.status_code, 543)
