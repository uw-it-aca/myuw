from django.test import TransactionTestCase
from django.conf import settings
from myuw.dao.user import get_migration_preference,\
    set_preference_to_old_myuw, set_preference_to_new_myuw,\
    display_onboard_message, has_legacy_preference,\
    is_oldmyuw_user, set_no_onboard_message
from myuw.test import get_request_with_user


class TestUserDao(TransactionTestCase):

    def test_legacy_preference(self):
        req = get_request_with_user('nobody')
        # default value
        migration_preference = get_migration_preference(req)
        self.assertFalse(migration_preference.use_legacy_site)
        self.assertFalse(has_legacy_preference(req))

        set_preference_to_old_myuw(req)
        self.assertTrue(get_migration_preference(req).use_legacy_site)
        self.assertTrue(has_legacy_preference(req))

        set_preference_to_new_myuw(req)
        self.assertFalse(get_migration_preference(req).use_legacy_site)
        self.assertFalse(has_legacy_preference(req))

    def set_no_onboard_message(self):
        req = get_request_with_user('nobody')
        # default value
        migration_preference = get_migration_preference(req)
        self.assertTrue(migration_preference.display_onboard_message)
        self.assertTrue(display_onboard_message(req))

        set_no_onboard_message(req)
        self.assertFalse(display_onboard_message(req))

    def test_is_oldmyuw_user(self):
        req = get_request_with_user('jerror')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('none')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('billseata')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('jnew')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('javerage')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('seagrad')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('curgrad')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('faculty')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('retirestaff')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('japplicant')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('jpce')
        self.assertFalse(is_oldmyuw_user(req))
