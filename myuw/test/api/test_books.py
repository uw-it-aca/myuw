# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, require_url, fdao_bookstore_override
from myuw.test import get_request_with_user, get_request_with_date


VERBACOMPARE_URL_PREFIX = 'http://uw-seattle.verbacompare.com'
IMAGE_URL_PREFIX = 'www7.bookstore.washington.edu/MyUWImage.taf'


@fdao_bookstore_override
class TestApiBooks(MyuwApiTest):
    '''Tests textbooks api'''

    @require_url('myuw_home')
    def test_javerage_books(self):
        self.set_user('javerage')
        response = self.get_response_by_reverse(
            'myuw_book_api',
            kwargs={'year': 2013,
                    'quarter': 'spring',
                    'summer_term': ''})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["order_url"],
                          ('http://www.ubookstore.com/adoption-search' +
                           '-results?ccid=9335,1132,5320,2230,4405'))

        self.assertGreaterEqual(len(data['18532']), 1)
        book = data['18532'][0]
        self.assertEquals(
            book["cover_image_url"],
            ("%s?isbn=9780878935970&key=46c9ef715edb2ec69517e2c8e6ec9c18" %
             IMAGE_URL_PREFIX))
        self.assertEquals(len(book["authors"]), 1)
        self.assertTrue(book["is_required"])
        self.assertIsNone(book["price"])
        self.assertIsNone(book["used_price"])
        self.assertEquals(book["isbn"], '9780878935970')
        self.assertEquals(book["notes"], 'required')
        self.assertIsNone(book["price"])

    @require_url('myuw_home')
    def test_no_sche_books(self):
        self.set_user('staff')
        response = self.get_response_by_reverse(
            'myuw_book_api',
            kwargs={'year': 2013,
                    'quarter': 'spring',
                    'summer_term': ''})
        self.assertEquals(response.status_code, 404)

    @require_url('myuw_home')
    def test_invalid_sln_books(self):
        self.set_user('jeos')
        response = self.get_response_by_reverse(
            'myuw_book_api',
            kwargs={'year': 2013,
                    'quarter': 'spring',
                    'summer_term': ''})
        self.assertEquals(response.status_code, 404)
