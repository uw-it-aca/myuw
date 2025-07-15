# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, fdao_bookstore_override


VERBACOMPARE_URL_PREFIX = 'http://uw-seattle.verbacompare.com'
IMAGE_URL_PREFIX = 'www7.bookstore.washington.edu/MyUWImage.taf'


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
