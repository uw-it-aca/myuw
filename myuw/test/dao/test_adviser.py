# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.adviser import get_academic_advisers
from myuw.test import get_request_with_user


class TestAdviserDao(TestCase):

    def test_get_normal_case(self):
        advisers = get_academic_advisers(
            get_request_with_user('javerage')
        )
        self.assertEquals(len(advisers), 5)

    def test_get_error_case(self):
        self.assertRaises(DataFailureException,
                          get_academic_advisers,
                          get_request_with_user('javg002'))

        self.assertRaises(DataFailureException,
                          get_academic_advisers,
                          get_request_with_user('jinter'))
