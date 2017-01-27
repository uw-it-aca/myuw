from django.test import TransactionTestCase
from django.conf import settings
from myuw.models import UserMigrationPreference
from myuw.dao.user import set_preference_to_new_myuw,\
    set_preference_to_old_myuw, has_legacy_preference, has_newmyuw_preference,\
    is_optin_user, is_oldmyuw_user, is_oldmyuw_mobile_user
from myuw.test import get_request_with_user


class TestUserDao(TransactionTestCase):

    def test_is_optin_user(self):
        self.assertTrue(is_optin_user('javerage'))
        self.assertTrue(is_optin_user('seagrad'))
        self.assertFalse(is_optin_user('nobody'))

    def test_has_legacy_preference(self):
        self.assertFalse(has_legacy_preference('nobody'))

        with self.assertRaises(UserMigrationPreference.DoesNotExist):
            UserMigrationPreference.objects.get(username='iprefold')

        set_preference_to_old_myuw('iprefold')
        obj = UserMigrationPreference.objects.get(username='iprefold')
        self.assertTrue(obj.use_legacy_site)
        self.assertTrue(has_legacy_preference('iprefold'))

    def test_has_newmyuw_preference(self):
        self.assertFalse(has_newmyuw_preference('nobody'))

        with self.assertRaises(UserMigrationPreference.DoesNotExist):
            UserMigrationPreference.objects.get(username='iprefnew')

        set_preference_to_new_myuw('iprefnew')
        self.assertTrue(has_newmyuw_preference('iprefnew'))
        obj = UserMigrationPreference.objects.get(username='iprefnew')
        self.assertFalse(obj.use_legacy_site)

    def test_is_oldmyuw_user(self):
        get_request_with_user('nobody')
        self.assertTrue(is_oldmyuw_user())

        get_request_with_user('jnew')
        self.assertFalse(is_oldmyuw_user())

        get_request_with_user('javerage')
        self.assertFalse(is_oldmyuw_user())

        # cur grad opt_in
        get_request_with_user('seagrad')
        self.assertFalse(is_oldmyuw_user())

        get_request_with_user('currgrad')
        self.assertTrue(is_oldmyuw_user())

        get_request_with_user('staff')
        self.assertTrue(is_oldmyuw_user())

        get_request_with_user('faculty')
        self.assertTrue(is_oldmyuw_user())

    def test_is_oldmyuw_mobile_user(self):
        get_request_with_user('javerage')
        self.assertFalse(is_oldmyuw_mobile_user())

        get_request_with_user('jinter')
        self.assertFalse(is_oldmyuw_mobile_user())

        get_request_with_user('seagrad')
        self.assertFalse(is_oldmyuw_mobile_user())

        get_request_with_user('none')
        self.assertFalse(is_oldmyuw_mobile_user())

        get_request_with_user('currgrad')
        self.assertTrue(is_oldmyuw_mobile_user())

        get_request_with_user('faculty')
        self.assertTrue(is_oldmyuw_mobile_user())

        get_request_with_user('staff')
        self.assertTrue(is_oldmyuw_mobile_user())
