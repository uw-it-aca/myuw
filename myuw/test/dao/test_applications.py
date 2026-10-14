# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from uw_sdbmyuw.util import fdao_sdbmyuw_override

from myuw.dao.applications import get_applications
from myuw.test import get_request_with_user


@fdao_sdbmyuw_override
class TestApplications(TestCase):

    def test_get_with_data(self):
        applications = get_applications(
            get_request_with_user('japplicant')
        )
        self.assertEqual(len(applications), 3)

    def test_get_with_missing_key(self):
        applications = get_applications(
            get_request_with_user("none")
        )
        self.assertEqual(len(applications), 0)

    def test_get_error_case(self):
        self.assertRaises(DataFailureException,
                          get_applications,
                          get_request_with_user('jerror'))
