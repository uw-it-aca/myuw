from django.test import TransactionTestCase
from django.conf import settings
from myuw.dao.user_pref import get_migration_preference,\
    set_preference_to_old_myuw, set_preference_to_new_myuw,\
    set_no_onboard_message, turn_off_pop_up
from myuw.test import get_request_with_user


class TestUserPrefDao(TransactionTestCase):

    def test_legacy_preference(self):
        req = get_request_with_user('nobody')
        # default value
        migration_preference = get_migration_preference(req)
        self.assertIsNotNone(migration_preference.json_data())
        self.assertIsNotNone(str(migration_preference))
        self.assertFalse(migration_preference.use_legacy_site)

        pref = set_preference_to_old_myuw(req)
        self.assertTrue(pref.use_legacy_site)

        pref = set_preference_to_new_myuw(req)
        self.assertFalse(pref.use_legacy_site)

    def test_set_no_onboard_message(self):
        req = get_request_with_user('nobody')
        # default value
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

    def is_oldmyuw_user(self, req):
        migration_preference = get_migration_preference(req)
        return migration_preference.use_legacy_site

    def test_is_oldmyuw_user(self):
        req = get_request_with_user('jerror')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('none')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('billseata')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('jnew')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('javerage')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('seagrad')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('curgrad')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('faculty')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('retirestaff')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('japplicant')
        self.assertFalse(self.is_oldmyuw_user(req))

        req = get_request_with_user('jpce')
        self.assertFalse(self.is_oldmyuw_user(req))
