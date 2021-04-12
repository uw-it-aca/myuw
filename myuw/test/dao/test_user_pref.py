# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TransactionTestCase
from django.conf import settings
from myuw.dao.user_pref import set_no_onboard_message, turn_off_pop_up,\
    get_migration_preference
from myuw.test import get_request_with_user


class TestUserPrefDao(TransactionTestCase):

    def test_set_no_onboard_message(self):
        req = get_request_with_user('nobody')
        self.assertFalse(hasattr(req, "migration_preference"))
        # default value
        migration_preference = get_migration_preference(req)
        self.assertTrue(hasattr(req, "migration_preference"))

        migration_preference = get_migration_preference(req)
        self.assertTrue(migration_preference.display_onboard_message)

        pref = set_no_onboard_message(req)
        self.assertFalse(pref.display_onboard_message)

    def test_turn_off_pop_up(self):
        req = get_request_with_user('nobody')
        migration_preference = get_migration_preference(req)
        self.assertTrue(migration_preference.display_pop_up)

        pref = turn_off_pop_up(req)
        self.assertFalse(pref.display_pop_up)
