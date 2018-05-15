from commonconf import override_settings
from django.test import TestCase
from myuw.authorization import validate_netid, INVALID_STRING, NO_USER,\
    can_override_user, is_myuw_admin
from myuw.test import get_request_with_user


@override_settings(USERSERVICE_VALIDATION_MODULE=
                   "myuw.authorization.validate_netid",
                   USERSERVICE_OVERRIDE_AUTH_MODULE=
                   "myuw.authorization.can_override_user",
                   RESTCLIENTS_ADMIN_AUTH_MODULE=
                   "myuw.authorization.can_proxy_restclient")
class TestValidation(TestCase):

    def test_validation(self):
        self.assertEquals(validate_netid("javerage"), None)
        self.assertEquals(validate_netid(""), NO_USER)
        self.assertEquals(validate_netid("jaVeRaGe"), None)
        self.assertEquals(validate_netid("a_canvas"), None)
        self.assertEquals(validate_netid("99invalid"), INVALID_STRING)
        self.assertEquals(validate_netid("thisisfartoolongtobeanetid"),
                          INVALID_STRING)

    def test_can_override_user(self):
        req = get_request_with_user("faculty")
        self.assertFalse(hasattr(req, "can_override_user"))
        self.assertTrue(can_override_user(req))
        self.assertTrue(req.can_override_user)

    def test_not_overrider(self):
        req = get_request_with_user("billsea")
        self.assertFalse(hasattr(req, "can_override_user"))
        self.assertFalse(can_override_user(req))
        self.assertTrue(hasattr(req, "can_override_user"))

    def test_is_myuw_admin(self):
        req = get_request_with_user("javerage")
        self.assertFalse(hasattr(req, "can_proxy_restclient"))
        self.assertTrue(is_myuw_admin(req))
        self.assertTrue(req.can_proxy_restclient)

    def test_not_myuw_admin(self):
        req = get_request_with_user("faculty")
        self.assertFalse(hasattr(req, "can_proxy_restclient"))
        self.assertFalse(is_myuw_admin(req))
        self.assertTrue(hasattr(req, "can_proxy_restclient"))
