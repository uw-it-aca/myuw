# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, require_url, fdao_sws_override


@fdao_sws_override
@require_url('myuw_other_quarters_api')
class TestOtherQuarters(MyuwApiTest):

    def get_oquarters_response(self):
        return self.get_response_by_reverse('myuw_other_quarters_api')

    def test_javerage_oquarters(self):
        self.set_user('javerage')
        response = self.get_oquarters_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data["terms"][0]["has_registration"])
        self.assertFalse(data["next_term_data"]["has_registration"])

        self.set_date("2013-05-15")
        response = self.get_oquarters_response()
        data = json.loads(response.content)
        self.assertEquals(data["next_term_data"]["has_registration"], True)
        self.assertEquals(data["next_term_data"]["quarter"], "Autumn")
        self.assertEquals(data["next_term_data"]["year"], 2013)

        self.assertEquals(len(data["terms"]), 3)
        self.assertEquals(data['next_term_data']['label'], '2013,autumn')
        self.assertEquals(data["terms"][0]['summer_term'], 'a-term')
        self.assertEquals(data["terms"][0]['year'], 2013)
        self.assertEquals(data["terms"][0]['quarter'], 'Summer')
        self.assertEquals(data["terms"][0]['credits'], '2.0')
        self.assertEquals(data["terms"][0]['section_count'], 2)
        self.assertEquals(data["terms"][0]['url'], '/2013,summer,a-term')
        self.assertTrue(data["terms"][0]['highlight'])
        self.assertTrue(data["terms"][0]['has_registration'])
        self.assertTrue(data["highlight_future_quarters"])

    def test_error(self):
        self.set_user('jerror')
        response = self.get_oquarters_response()
        self.assertEquals(response.status_code, 543)
