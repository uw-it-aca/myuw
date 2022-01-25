# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.degree import get_degrees, get_degrees_json
from myuw.test import get_request_with_user

DEGREE_DATA = {
    'degrees': [{
        'campus': 'SEATTLE',
        'diploma_mail': 0,
        'diploma_mail_to_local_address': False,
        'has_applied': True,
        'is_admin_hold': False,
        'is_granted': False,
        'is_incomplete': False,
        'is_degree_earned_term': True,
        'before_degree_earned_term': False,
        'during_april_may': True,
        'level': 1,
        'name_on_diploma': 'John Joseph Average',
        'quarter': 'spring',
        'status': 5,
        'title': 'BACHELOR OF ARTS (POLITICAL SCIENCE)',
        'type': 1,
        'year': 2013}],
    'error_code': None}

class TestAdviserDao(TestCase):

    def test_get_degrees(self):
        degrees = get_degrees(
            get_request_with_user('javerage')
        )
        self.assertEquals(len(degrees), 1)

        self.assertRaises(DataFailureException,
                          get_degrees,
                          get_request_with_user('jerror'))

        self.assertRaises(DataFailureException,
                          get_degrees,
                          get_request_with_user('jinter'))

    def test_get_degrees_json(self):
        degree_data = get_degrees_json(
            get_request_with_user('javerage')
        )
        self.assertEquals(degree_data, DEGREE_DATA)

        degree_data = get_degrees_json(
            get_request_with_user('jbothell')
        )
        self.assertEquals(
            degree_data,
            {'degrees': None, 'error_code': 404})
