# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import (
    MyuwApiTest, require_url, fdao_sws_override, fdao_pws_override)


url_name = "myuw_prev_unfinished_schedule"


@fdao_pws_override
@fdao_sws_override
@require_url(url_name)
class TestStudUnfinishedPrevQuarClasSche(MyuwApiTest):

    def get_prev_unfinished_schedule(self, user=None, date=None):
        if user:
            self.set_user(user)
        if date:
            self.set_date(date)
        return self.get_response_by_reverse(url_name)

    def test_404(self):
        response = self.get_prev_unfinished_schedule('javerage')
        self.assertEqual(response.content, b'Data not found')
        self.assertEqual(response.status_code, 404)

    def test_no_prev_terms(self):
        response = self.get_prev_unfinished_schedule('jpce',
                                                     '2013-08-08 00:00:01')
        self.assertEqual(response.content, b'Data not found')
        self.assertEqual(response.status_code, 404)

    def test_one_prev_term(self):
        response = self.get_prev_unfinished_schedule('jpce')
        self.assertEqual(response.status_code, 200)
        ret_data = json.loads(response.content)

        self.assertEqual(len(ret_data), 1)
        data = ret_data[0]
        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Winter')
        self.assertEqual(len(data["sections"]), 2)

        com = self.get_section(data, 'COM', '201', 'A')
        self.assertEqual(com['start_date'], '2013-01-30')
        self.assertEqual(com['end_date'], '2013-04-29')
        self.assertFalse(com["is_ended"])

        psych = self.get_section(data, 'PSYCH', '203', 'A')
        self.assertEqual(psych['start_date'], '2013-01-29')
        self.assertEqual(psych['end_date'], '2013-07-30')
        self.assertFalse(psych["is_ended"])

    def test_two_prev_terms(self):
        response = self.get_prev_unfinished_schedule('jpce',
                                                     '2013-06-24 00:00:01')
        self.assertEqual(response.status_code, 200)
        ret_data = json.loads(response.content)
        self.assertEqual(len(ret_data), 2)

        data = ret_data[0]
        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Winter')
        self.assertEqual(len(data["sections"]), 1)

        data = ret_data[1]
        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Spring')
        self.assertEqual(len(data["sections"]), 2)
