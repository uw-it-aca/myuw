# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.views.api.textbook import get_payment_quarter
from myuw.test import get_request_with_date
from myuw.test.api import MyuwApiTest, require_url, fdao_bookstore_override

VERBACOMPARE_URL_PREFIX = 'http://uw-seattle.verbacompare.com'
IMAGE_URL_PREFIX = 'www7.bookstore.washington.edu/MyUWImage.taf'


@fdao_bookstore_override
class TestApiBooks(MyuwApiTest):
    '''Tests textbooks api'''

    @require_url('myuw_book_api')
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
        self.set_user('billtac')  # MUWM-5311
        response = self.get_response_by_reverse(
            'myuw_book_api',
            kwargs={'year': 2013,
                    'quarter': 'spring',
                    'summer_term': ''})
        self.assertEquals(response.status_code, 200)

    @require_url('myuw_iacourse_digital_material_api')
    def test_digital_material_api(self):
        self.set_user('javerage')
        response = self.get_response_by_reverse(
            'myuw_iacourse_digital_material')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["quarter"], "spring")
        self.assertEquals(data["year"], 2013)
        self.assertEquals(data["balance"], 219.85)

        response = self.get_response_by_reverse(
            'myuw_iacourse_digital_material_api',
            kwargs={'year': 2013,
                    'quarter': 'spring'})
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["quarter"], "spring")
        self.assertEquals(data["year"], 2013)
        self.assertEquals(data["balance"], 219.85)

        response = self.get_response_by_reverse(
            'myuw_iacourse_digital_material_api',
            kwargs={'year': 2013,
                    'quarter': 'autumn'})
        self.assertEquals(response.status_code, 404)

        response = self.get_response_by_reverse(
            'myuw_iacourse_digital_material_api',
            kwargs={'year': 2013,
                    'quarter': 'winter'})
        self.assertEquals(response.status_code, 404)

        self.set_user('jbothell')
        response = self.get_response_by_reverse(
            'myuw_iacourse_digital_material_api',
            kwargs={'year': 2013,
                    'quarter': 'spring'})
        self.assertEquals(response.status_code, 404)

        response = self.get_response_by_reverse(
            'myuw_iacourse_digital_material')
        self.assertEquals(response.status_code, 404)

    def test_get_payment_quarter(self):
        request = get_request_with_date('2013-06-18')
        q = get_payment_quarter(request)
        self.assertEquals(q.quarter, "spring")

        request = get_request_with_date('2013-06-19')
        q = get_payment_quarter(request)
        self.assertEquals(q.quarter, "summer")

        request = get_request_with_date('2013-09-19')
        q = get_payment_quarter(request)
        self.assertEquals(q.quarter, "autumn")

        request = get_request_with_date('2013-12-27')
        q = get_payment_quarter(request)
        self.assertEquals(q.quarter, "winter")
