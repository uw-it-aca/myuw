# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.views.api.textbook import get_payment_quarter
from myuw.test import get_request_with_date
from myuw.test.api import MyuwApiTest, fdao_bookstore_override

VERBACOMPARE_URL_PREFIX = "http://uw-seattle.verbacompare.com"
IMAGE_URL_PREFIX = "www7.bookstore.washington.edu/MyUWImage.taf"


@fdao_bookstore_override
class TestApiBooks(MyuwApiTest):
    """Tests textbooks api"""

    def test_textbooks(self):
        self.set_user("javerage")
        response = self.get_response_by_reverse(
            "myuw_book_api",
            kwargs={"year": 2013,
                    "quarter": "spring",
                    "summer_term": ""})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 6)

    def test_textbooks_404(self):
        self.set_user("javerage")
        response = self.get_response_by_reverse(
            "myuw_book_api",
            kwargs={"year": 2013,
                    "quarter": "autumn",
                    "summer_term": ""})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsNotNone(data.get('13519'))
        self.assertIsNotNone(data.get('13870'))
        self.assertIsNotNone(data.get("order_url"))

    def test_noschedule(self):
        self.set_user("billtac")  # MUWM-5311
        response = self.get_response_by_reverse(
            "myuw_book_api",
            kwargs={"year": 2013,
                    "quarter": "spring",
                    "summer_term": ""})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, {})

    def test_digital_material_api(self):
        self.set_user("javerage")
        response = self.get_response_by_reverse(
            "myuw_iacourse_digital_material")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["quarter"], "spring")
        self.assertEqual(data["year"], 2013)
        self.assertEqual(data["balance"], 219.85)

        response = self.get_response_by_reverse(
            "myuw_iacourse_digital_material_api",
            kwargs={"year": 2013,
                    "quarter": "spring"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["quarter"], "spring")
        self.assertEqual(data["year"], 2013)
        self.assertEqual(data["balance"], 219.85)

        response = self.get_response_by_reverse(
            "myuw_iacourse_digital_material_api",
            kwargs={"year": 2013,
                    "quarter": "autumn"})
        self.assertEqual(response.status_code, 404)

        response = self.get_response_by_reverse(
            "myuw_iacourse_digital_material_api",
            kwargs={"year": 2013,
                    "quarter": "winter"})
        self.assertEqual(response.status_code, 404)

        self.set_user("jbothell")
        response = self.get_response_by_reverse(
            "myuw_iacourse_digital_material_api",
            kwargs={"year": 2013,
                    "quarter": "spring"})
        self.assertEqual(response.status_code, 404)

        response = self.get_response_by_reverse(
            "myuw_iacourse_digital_material")
        self.assertEqual(response.status_code, 404)

    def test_get_payment_quarter(self):
        request = get_request_with_date("2013-06-18")
        q = get_payment_quarter(request)
        self.assertEqual(q.quarter, "spring")

        request = get_request_with_date("2013-06-19")
        q = get_payment_quarter(request)
        self.assertEqual(q.quarter, "summer")

        request = get_request_with_date("2013-09-19")
        q = get_payment_quarter(request)
        self.assertEqual(q.quarter, "autumn")

        request = get_request_with_date("2013-12-27")
        q = get_payment_quarter(request)
        self.assertEqual(q.quarter, "winter")
