from django.test import TestCase
from myuw.dao.uwnetid import (is_staff, is_faculty, get_subscriptions,
                              get_email_forwarding_for_current_user,
                              is_clinician, is_2fa_permitted,
                              is_retired_staff, is_alumni, is_past_staff,
                              is_past_faculty, is_past_clinician,
                              is_past_undergrad, is_past_grad, is_past_pce)
from myuw.test import get_request_with_user, fdao_uwnetid_override


@fdao_uwnetid_override
class TestUWNetidDao(TestCase):

    def test_subscriptions_prefetch(self):
        req = get_request_with_user('javerage')
        self.assertFalse(hasattr(req, "myuwnetid_subscriptions"))
        subs_dict = get_subscriptions(req)
        self.assertIsNotNone(req.myuwnetid_subscriptions)
        self.assertIsNotNone(req.myuwnetid_subscriptions[105])
        self.assertIsNotNone(req.myuwnetid_subscriptions[60])
        self.assertIsNotNone(req.myuwnetid_subscriptions[64])

    def test_email_forwarding(self):
        req = get_request_with_user('javerage')
        forward = get_email_forwarding_for_current_user(req)
        self.assertEquals(forward.fwd, "javerage@gamail.uw.edu")

        req = get_request_with_user('nobody')
        forward = get_email_forwarding_for_current_user(req)
        self.assertIsNone(forward.fwd)
        self.assertTrue(forward.permitted)
        self.assertFalse(forward.is_active())

    def test_get_subscriptions(self):
        req = get_request_with_user('javerage')
        self.assertFalse(is_clinician(req))
        self.assertFalse(is_faculty(req))
        self.assertFalse(is_staff(req))
        self.assertTrue(is_2fa_permitted(req))

    def test_is_2fa_permitted(self):
        req = get_request_with_user('bill')
        self.assertTrue(is_2fa_permitted(req))

        req = get_request_with_user('jbothell')
        self.assertFalse(is_2fa_permitted(req))

    def test_clinician(self):
        req = get_request_with_user('staff')
        self.assertTrue(is_clinician(req))

    def test_faculty(self):
        req = get_request_with_user('bill')
        self.assertTrue(is_faculty(req))
        self.assertTrue(is_past_grad(req))
        self.assertTrue(is_alumni(req))

    def test_staff(self):
        req = get_request_with_user('staff')
        self.assertTrue(is_staff(req))
        self.assertFalse(is_past_grad(req))
        self.assertFalse(is_past_undergrad(req))
        self.assertFalse(is_past_pce(req))

        req = get_request_with_user('japplicant')
        self.assertTrue(is_staff(req))

    def test_retiree(self):
        req = get_request_with_user('retirestaff')
        self.assertFalse(is_staff(req))
        self.assertTrue(is_past_grad(req))
        self.assertTrue(is_past_undergrad(req))
        self.assertTrue(is_past_pce(req))
        self.assertTrue(is_retired_staff(req))

    def test_alumni(self):
        req = get_request_with_user('javerage')
        self.assertTrue(is_alumni(req))
        self.assertTrue(is_past_pce(req))

        req = get_request_with_user('jalum')
        self.assertTrue(is_alumni(req))
        self.assertTrue(is_past_undergrad(req))
