# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.stud_eme_contact import get_eme_contacts
from myuw.test import get_request_with_user


class TestStudEmeContacts(TestCase):

    def test_get_normal_case(self):
        eme_contacts = get_eme_contacts(
            get_request_with_user('javerage')
        )
        self.assertEqual(len(eme_contacts), 1)

    def test_get_error_case(self):
        self.assertRaises(DataFailureException,
                          get_eme_contacts,
                          get_request_with_user('jerror'))

        self.assertRaises(DataFailureException,
                          get_eme_contacts,
                          get_request_with_user('none'))
