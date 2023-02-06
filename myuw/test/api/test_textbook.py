# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import require_url, MyuwApiTest


@require_url('myuw_current_book')
class TestInstructorTextbookCur(MyuwApiTest):

    def test_get(self):
        self.set_user('billpce')
        self.set_date("2013-10-16 09:00:00")
        resp = self.get_response_by_reverse('myuw_current_book')
        data = json.loads(resp.content)
        self.assertEqual(data, {'21838': []})
