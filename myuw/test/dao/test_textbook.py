# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao.registration import get_schedule_by_term
from uw_sws.models import Term
from restclients_core.exceptions import DataFailureException
from myuw.dao.textbook import (
    get_textbook_by_schedule, get_order_url_by_schedule,
    get_iacourse_status)
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.dao.term import get_current_quarter
from myuw.test import get_request_with_user, get_request_with_date


class TestTextbooks(TestCase):

    def test_get_by_schedule(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-08-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)

        books = get_textbook_by_schedule(schedule)
        self.assertEqual(len(books), 1)
        self.assertEqual(
            books[13833][0].title,
            "2 P/S Tutorials In Introductory Physics")

    def test_get_order_url_by_schedule(self):
        req = get_request_with_user('javerage')
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
        returned_link = get_order_url_by_schedule(schedule)

        expected_link = ('http://www.ubookstore.com/adoption-search-results?' +
                         'ccid=9335,1132,5320,2230,4405')
        self.assertEqual(returned_link, expected_link)

        req = get_request_with_user('javerage',
                                    get_request_with_date("2014-02-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
        self.assertRaises(DataFailureException,
                          get_order_url_by_schedule,
                          schedule)

    def test_get_inst_textbook(self):
        req = get_request_with_user('billpce',
                                    get_request_with_date("2013-10-01"))
        schedule = get_instructor_schedule_by_term(req)

        books = get_textbook_by_schedule(schedule)
        self.assertEqual(len(books), 1)

    def test_get_uwt_inst_textbook(self):
        req = get_request_with_user('billtac',
                                    get_request_with_date("2013-04-01"))
        schedule = get_instructor_schedule_by_term(req)
        self.assertEqual(len(schedule.sections), 3)
        books = get_textbook_by_schedule(schedule)
        self.assertEqual(len(books), 0)

    def test_get_iacourse_status(self):
        req = get_request_with_user(
            'javerage', get_request_with_date("2013-05-01"))
        term = get_current_quarter(req)
        data = get_iacourse_status(req, term)
        self.assertIsNotNone(data.json_data())

        req = get_request_with_user(
            'javerage', get_request_with_date("2013-06-25"))
        term = get_current_quarter(req)
        data = get_iacourse_status(req, term)
        self.assertIsNotNone(data.json_data())

        req = get_request_with_user(
            'javerage', get_request_with_date("2013-12-31"))
        term = get_current_quarter(req)
        data = get_iacourse_status(req, term)
        self.assertIsNone(data)
