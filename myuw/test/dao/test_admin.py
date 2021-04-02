# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao import get_netid_of_original_user
from myuw.dao.admin import is_admin, can_override
from myuw.test import fdao_gws_override, get_request_with_user, auth_override


@fdao_gws_override
@auth_override
class TestAdminDao(TestCase):

    def test_is_admin(self):
        get_request_with_user("javerage")
        self.assertEqual(get_netid_of_original_user(), "javerage")
        self.assertTrue(is_admin())
        self.assertTrue(can_override())

    def test_can_override(self):
        get_request_with_user("faculty")
        self.assertFalse(is_admin())
        self.assertTrue(can_override())

    def test_not_both(self):
        get_request_with_user("none")
        self.assertFalse(is_admin())
        self.assertFalse(can_override())

    def test_except(self):
        get_request_with_user("jerror")
        self.assertFalse(is_admin())
        self.assertFalse(can_override())
