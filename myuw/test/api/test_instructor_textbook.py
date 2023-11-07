# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import require_url, MyuwApiTest
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.views.api.textbook import (
    get_textbook_by_schedule, _get_schedule_textbooks, index_by_sln)
from myuw.test import get_request_with_user, get_request_with_date


@require_url('myuw_current_book')
class TestInstructorTextbookCur(MyuwApiTest):

    def test_get(self):
        self.set_user('billpce')
        self.set_date("2013-10-16 09:00:00")
        resp = self.get_response_by_reverse('myuw_current_book')
        data = json.loads(resp.content)
        self.assertEqual(data, {'21838': []})

    def test_get_uwt_inst_textbook(self):
        # MUWM-5311: uwt no longer has books
        req = get_request_with_user('billtac',
                                    get_request_with_date("2013-04-01"))
        schedule = get_instructor_schedule_by_term(req)
        bkData = get_textbook_by_schedule(schedule)
        self.assertEqual(bkData, {})
        self.assertEqual(index_by_sln(bkData), {})

        data = _get_schedule_textbooks(schedule)
        self.assertEqual(data, {})

        self.set_user('billtac')
        resp = self.get_response_by_reverse('myuw_current_book')
        data = json.loads(resp.content)
        self.assertEqual(data, {})
