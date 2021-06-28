# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.attestation import get_covid19_vaccination
from myuw.test import get_request_with_user


class TestCovid19VaccinationDao(TestCase):

    def test_get_normal_case(self):
        result = get_covid19_vaccination(
            get_request_with_user('javerage')
        )
        self.assertIsNotNone(result)

    def test_get_error_case(self):
        self.assertRaises(DataFailureException,
                          get_covid19_vaccination,
                          get_request_with_user('jerror'))

        self.assertRaises(DataFailureException,
                          get_covid19_vaccination,
                          get_request_with_user('jalum'))
