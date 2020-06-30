from django.test import TestCase
from myuw.dao.uwnetid import (
    get_subscriptions, get_email_forwarding_for_current_user,
    is_2fa_permitted, BlockedNetidErr)
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
        self.assertRaises(
            BlockedNetidErr,
            get_email_forwarding_for_current_user, req)

        req = get_request_with_user('none')
        forward = get_email_forwarding_for_current_user(req)
        self.assertIsNone(forward.fwd)
        self.assertTrue(forward.permitted)
        self.assertFalse(forward.is_active())

    def test_get_subscriptions(self):
        req = get_request_with_user('javerage')
        self.assertTrue(is_2fa_permitted(req))

    def test_is_2fa_permitted(self):
        req = get_request_with_user('bill')
        self.assertTrue(is_2fa_permitted(req))

        req = get_request_with_user('jbothell')
        self.assertFalse(is_2fa_permitted(req))
