# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, require_url, fdao_sws_override


@fdao_sws_override
@require_url('myuw_home')
class TestFutureSchedule(MyuwApiTest):

    def get_schedule(self, **kwargs):
        return self.get_response_by_reverse(
            'myuw_future_schedule_api',
            kwargs=kwargs,)

    def get_schedule_summer(self, **kwargs):
        return self.get_response_by_reverse(
            'myuw_future_summer_schedule_api',
            kwargs=kwargs,)

    def test_javerage_future(self):
        self.set_user('javerage')
        response = self.get_schedule(year=2013, quarter='autumn')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data["sections"]), 2)

        response = self.get_schedule(year=2015, quarter='autumn')
        self.assertEqual(response.status_code, 404)

        response = self.get_schedule_summer(
            year=2013, quarter='summer', summer_term='a-term')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["sections"]), 2)

        response = self.get_schedule_summer(
            year=2013, quarter='summer', summer_term='b-term')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["sections"]), 2)

        response = self.get_schedule(year=2013, quarter='summer')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["sections"]), 3)

    def test_error(self):
        self.set_user('jerror')
        response = self.get_schedule(year=2013, quarter='summer')
        self.assertEqual(response.status_code, 543)

        response = self.get_schedule(year=2013, quarter='autumn')
        self.assertEqual(response.status_code, 404)

    def test_past_quarter(self):
        self.set_user('javerage')
        self.set_date("2013-04-01")
        response = self.get_schedule(year=2013, quarter='winter')
        self.assertEqual(response.status_code, 410)
