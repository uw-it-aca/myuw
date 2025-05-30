# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
import json
from myuw.test.api import MyuwApiTest, require_url, fdao_ias_override


@fdao_ias_override
@require_url('myuw_iasystem_api', 'IAS urls not configured')
class TestIasystemApi(MyuwApiTest):

    def get_ias_response(self):
        return self.get_response_by_reverse('myuw_iasystem_api')

    def test_javerage_normal_cases(self):
        response = self.get_ias_response()
        self.assertEqual(response.status_code, 302)

        self.set_user('javerage')
        response = self.get_ias_response()
        self.assertEqual(response.status_code, 404)

        # after show date 2013 Spring
        self.set_date('2013-05-31')
        response = self.get_ias_response()
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Spring')
        self.assertEqual(len(data["sections"]), 5)

        # before show date
        self.set_date('2013-07-16')
        response = self.get_ias_response()
        self.assertEqual(response.status_code, 404)

        # after show date
        self.set_date('2013-07-17')
        response = self.get_ias_response()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Summer')
        self.assertEqual(len(data["sections"]), 2)
        eval_data = data["sections"][0]["evaluation_data"]
        self.assertEqual(len(eval_data), 0)
        eval_data = data["sections"][1]["evaluation_data"]
        self.assertEqual(len(eval_data), 0)

    def test_eight_2013_spring(self):
        self.set_user('eight')
        self.set_date('2013-06-08')
        response = self.get_ias_response()

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Spring')
        self.assertEqual(len(data["sections"]), 8)

    def test_user_none(self):
        self.set_user('none')
        response = self.get_ias_response()
        self.assertEqual(response.status_code, 404)

    def test_missing_current_term(self):
        self.set_user('jerror')
        response = self.get_ias_response()
        self.assertEqual(response.status_code, 404)

    def test_summer_terms(self):
        self.set_user('javerage')
        self.set_date('2013-07-24')
        response = self.get_ias_response()
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Summer')
        self.assertEqual(data["summer_term"], "a-term")
        self.assertEqual(len(data["sections"]), 2)

        eval_data = data["sections"][0]["evaluation_data"]
        self.assertEqual(len(eval_data), 1)
        self.assertEqual(eval_data[0]['close_date'],
                         "2013-07-29T06:59:59+00:00")

        eval_data = data["sections"][1]["evaluation_data"]
        self.assertEqual(len(eval_data), 0)

        self.set_date('2013-08-27')
        response = self.get_ias_response()

        data = json.loads(response.content)
        self.assertEqual(data["summer_term"], "b-term")
        self.assertEqual(len(data["sections"]), 2)

        eval_data = data["sections"][0]["evaluation_data"]
        self.assertEqual(len(eval_data), 0)

        eval_data = data["sections"][1]["evaluation_data"]
        self.assertEqual(len(eval_data), 1)
        self.assertEqual(eval_data[0]['close_date'],
                         "2013-08-29T06:59:59+00:00")

    def test_jeos_2013_spring(self):
        self.set_user('jeos')
        self.set_date('2013-06-06')
        response = self.get_ias_response()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        eval_data = data["sections"][0]["evaluation_data"]
        self.assertEqual(len(eval_data), 1)
        self.assertEqual(eval_data[0]['instructors'][0]['instructor_name'],
                         'BILL Pce Instructor')
        self.assertEqual(eval_data[0]['close_date'],
                         '2013-06-08T06:59:59+00:00')
