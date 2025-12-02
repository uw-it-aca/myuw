# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.applications import get_applications
from myuw.test import get_request_with_user


class TestApplications(TestCase):

    def test_get_normal_case(self):
        applications = get_applications(
            get_request_with_user('japplicant')
        )
        self.assertEqual(len(applications), 3)

    def test_get_error_case(self):
        self.assertRaises(DataFailureException,
                          get_applications,
                          get_request_with_user('jerror'))

        self.assertRaises(DataFailureException,
                          get_applications,
                          get_request_with_user('none'))
