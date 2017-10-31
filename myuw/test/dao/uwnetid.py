from django.test import TestCase
from myuw.dao.uwnetid import (is_clinician, is_2fa_permitted,
                              get_subscriptions, is_faculty, is_staff)
from myuw.test import (fdao_uwnetid_override,
                       get_request, get_request_with_user)


@fdao_uwnetid_override
class TestUWNetid(TestCase):
    def setUp(self):
        get_request()

    def test_get_subscriptions(self):
        get_request_with_user('javerage')
        subs = get_subscriptions()
        self.assertIsNotNone(subs)
        self.assertEqual(len(subs), 2)

    def test_is_2fa_permitted(self):
        get_request_with_user('bill')
        self.assertTrue(is_2fa_permitted())
        self.assertFalse(is_clinician())

        get_request_with_user('javerage')
        self.assertTrue(is_2fa_permitted())
        self.assertFalse(is_clinician())

        get_request_with_user('eight')
        self.assertFalse(is_2fa_permitted())
        self.assertTrue(is_clinician())

    def test_is_clinician(self):
        get_request_with_user('staff')
        self.assertTrue(is_clinician())

    def test_is_faculty(self):
        get_request_with_user('bill')
        self.assertTrue(is_faculty())

    def test_is_staff(self):
        get_request_with_user('staff')
        self.assertTrue(is_staff())
