# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_home')
class TestMyPlanApi(MyuwApiTest):

    def _get_myplan_response(self, year, quarter):
        return self.get_response_by_reverse(
            'myuw_myplan_api',
            kwargs={'year': year, 'quarter': quarter}
        )

    def test_api_calls(self):
        self.set_user('eight')
        response = self._get_myplan_response(2013, 'summer')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['terms'][0]['year'], 2013)
        self.assertEquals(data['terms'][0]['quarter'], 'Summer')

        response = self._get_myplan_response(2013, 'autumn')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 0)

        self.set_user('jinter')
        response = self._get_myplan_response(2013, 'autumn')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data["terms"][0]["courses"]), 5)

    def test_error(self):
        self.set_user('jerror')
        response = self._get_myplan_response(2013, 'spring')
        self.assertEquals(response.status_code, 543)
