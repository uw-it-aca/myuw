from django.test import TransactionTestCase
from django.conf import settings
from myuw.models import UserMigrationPreference
from myuw.dao.user import set_preference_to_new_myuw,\
    set_preference_to_old_myuw, has_legacy_preference, has_newmyuw_preference,\
    is_optin_user, is_oldmyuw_user
from myuw.test import get_request_with_user


class TestUserDao(TransactionTestCase):

    def test_is_optin_user(self):
        self.assertTrue(is_optin_user('seagrad'))
        self.assertTrue(is_optin_user('jeos'))
        self.assertFalse(is_optin_user('nobody'))

    def test_has_legacy_preference(self):
        self.assertFalse(has_legacy_preference('nobody'))

        with self.assertRaises(UserMigrationPreference.DoesNotExist):
            UserMigrationPreference.objects.get(username='nobody')

        set_preference_to_old_myuw('nobody')
        obj = UserMigrationPreference.objects.get(username='nobody')
        self.assertTrue(obj.use_legacy_site)
        self.assertTrue(has_legacy_preference('nobody'))

    def test_has_newmyuw_preference(self):
        self.assertFalse(has_newmyuw_preference('nobody'))

        with self.assertRaises(UserMigrationPreference.DoesNotExist):
            UserMigrationPreference.objects.get(username='nobody')

        set_preference_to_new_myuw('nobody')
        self.assertTrue(has_newmyuw_preference('nobody'))
        obj = UserMigrationPreference.objects.get(username='nobody')
        self.assertFalse(obj.use_legacy_site)

    def test_is_oldmyuw_user(self):
        # in opt_in_list.txt
        req = get_request_with_user('none')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('billseata')
        self.assertFalse(is_oldmyuw_user(req))

        # undergrad student
        req = get_request_with_user('jnew')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('javerage')
        self.assertFalse(is_oldmyuw_user(req))

        # cur grad opt_in
        req = get_request_with_user('seagrad')
        self.assertFalse(is_oldmyuw_user(req))

        req = get_request_with_user('curgrad')
        self.assertTrue(is_oldmyuw_user(req))

        req = get_request_with_user('faculty')
        self.assertTrue(is_oldmyuw_user(req))

        req = get_request_with_user('retirestaff')
        self.assertTrue(is_oldmyuw_user(req))

        # applicant
        req = get_request_with_user('japplicant')
        self.assertFalse(is_oldmyuw_user(req))

        # C2
        req = get_request_with_user('jpce')
        self.assertFalse(is_oldmyuw_user(req))
