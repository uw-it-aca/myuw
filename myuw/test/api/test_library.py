# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, require_url, fdao_mylib_override


@fdao_mylib_override
@require_url('myuw_library_api')
class TestLibrary(MyuwApiTest):

    def get_library_response(self):
        return self.get_response_by_reverse('myuw_library_api')

    def test_javerage_books(self):
        self.set_user('javerage')
        response = self.get_library_response()
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data,
                         {'fines': 0,
                          'holds_ready': 1,
                          'items_loaned': 1,
                          'next_due': '2013-05-27T02:00:00+00:00'})

    def test_invalid_books(self):
        self.set_user('nodata')
        response = self.get_library_response()
        self.assertEqual(response.status_code, 404)

        self.set_user('none')
        response = self.get_library_response()
        self.assertEqual(response.status_code, 200)

        self.set_user('jerror')
        response = self.get_library_response()
        self.assertEqual(response.status_code, 543)
