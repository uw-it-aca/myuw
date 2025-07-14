# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.term import get_current_quarter
from myuw.dao.textbook import (
    get_textbook_json, get_iacourse_status)
from myuw.test import get_request_with_user, get_request_with_date


class TestTextbooks(TestCase):

    def test_get_textbooks(self):
        books = get_textbook_json("spring", {18529, 18532, 13830, 13833, 18545})
        self.assertEqual(len(books), 6)
        self.maxDiff = None
        self.assertEqual(
            books[13830],
            {
                "books": [
                    {
                        "authors": [{"name": "Mcdermott"}],
                        "cover_image_url": None,
                        "highest_price": 58.0,
                        "is_required": True,
                        "isbn": "9781256396362",
                        "lowest_price": 58.0,
                        "notes": None,
                        "price": 58.0,
                        "title": "Writ of BC",
                        "used_price": None,
                    }
                ],
                "course_id": "uws-phys-121-aq-123",
                "search_url": "https://ubookstore.com/pages/"
                + "adoption-search/course=",
            },
        )
        self.assertEqual(
            books[18529], 
            {"books": [],
             "course_id": "uws-phys-121-a-123",
             "search_url": "https://ubookstore.com/pages/" +
                           "adoption-search/course="})

        books = get_textbook_json("spring", {})
        self.assertEqual(books, {})

        books = get_textbook_json("spring", {18529, 18545, 18532, 13830, 13833, 15612})
        self.assertEqual(len(books), 7)
        # self.assertEqual(books, {})

    def test_get_iacourse_status(self):
        req = get_request_with_user(
            "javerage", get_request_with_date("2013-05-01"))
        term = get_current_quarter(req)
        data = get_iacourse_status(req, term)
        self.assertIsNotNone(data.json_data())

        req = get_request_with_user(
            "javerage", get_request_with_date("2013-06-25"))
        term = get_current_quarter(req)
        data = get_iacourse_status(req, term)
        self.assertIsNotNone(data.json_data())

        req = get_request_with_user(
            "javerage", get_request_with_date("2013-12-31"))
        term = get_current_quarter(req)
        data = get_iacourse_status(req, term)
        self.assertIsNone(data)
