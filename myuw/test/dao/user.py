from django.test import TransactionTestCase
from django.conf import settings
from myuw.dao.user import set_preference_to_new_myuw,\
    set_preference_to_old_myuw, has_legacy_preference, has_newmyuw_preference,\
    is_optin_user, is_fyp_thrive_viewer, is_oldmyuw_user
from myuw.test import get_request_with_user, FDAO_PWS


class TestUserDao(TransactionTestCase):

    def test_is_optin_user(self):
        self.assertTrue(is_optin_user('javerage'))
        self.assertTrue(is_optin_user('seagrad'))
        self.assertFalse(is_optin_user('nobody'))

    def test_is_fyp_thrive_viewer(self):
        self.assertTrue(is_fyp_thrive_viewer('javerage'))
        self.assertFalse(is_fyp_thrive_viewer('nobody'))

    def test_has_legacy_preference(self):
        set_preference_to_old_myuw('javerage')
        self.assertTrue(has_legacy_preference('javerage'))
        self.assertFalse(has_legacy_preference('nobody'))

    def test_has_newmyuw_preference(self):
        set_preference_to_new_myuw('iprefnew')
        self.assertTrue(has_newmyuw_preference('iprefnew'))
        self.assertFalse(has_newmyuw_preference('nobody'))

    def test_is_oldmyuw_user(self):
        get_request_with_user('jnew')
        self.assertFalse(is_oldmyuw_user())

        # grad but opt_in
        get_request_with_user('seagrad')
        self.assertFalse(is_oldmyuw_user())

        get_request_with_user('currgrad')
        self.assertTrue(is_oldmyuw_user())

        get_request_with_user('staff')
        self.assertTrue(is_oldmyuw_user())

        get_request_with_user('faculty')
        self.assertTrue(is_oldmyuw_user())
