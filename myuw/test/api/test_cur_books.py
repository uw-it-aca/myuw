# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, fdao_bookstore_override


@fdao_bookstore_override
class TestApiCurBooks(MyuwApiTest):

    def test_javerage_cur_term_books(self):
        self.set_user('javerage')
        response = self.get_response_by_reverse('myuw_current_book')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsNotNone(data.get("13833"))

    def test_eight_cur_term_books(self):
        self.set_user('eight')
        response = self.get_response_by_reverse('myuw_current_book')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsNotNone(data.get("11646"))

    def test_inst_nobook(self):
        self.set_user("billpce")
        self.set_date("2013-10-16 09:00:00")
        resp = self.get_response_by_reverse("myuw_current_book")
        data = json.loads(resp.content)
        self.assertEqual(
            data.get('21838'), {
                'books': [],
                'course_id': None,
                'search_url': None
            }
        )

    def test_inst_noschedule(self):
        self.set_user('jinter')
        resp = self.get_response_by_reverse('myuw_current_book')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data, {})
