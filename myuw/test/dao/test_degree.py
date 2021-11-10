# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.degree import get_degrees
from myuw.test import get_request_with_user


class TestAdviserDao(TestCase):

    def test_get_normal_case(self):
        degrees = get_degrees(
            get_request_with_user('javerage')
        )
        self.assertEquals(len(degrees), 1)

    def test_get_error_case(self):
        self.assertRaises(DataFailureException,
                          get_degrees,
                          get_request_with_user('jerror'))

        self.assertRaises(DataFailureException,
                          get_degrees,
                          get_request_with_user('jinter'))
