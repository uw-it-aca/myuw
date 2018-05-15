from commonconf import override_settings
from django.test import TestCase
from myuw.dao import get_netid_of_original_user
from myuw.dao.admin import is_admin, can_override
from myuw.test import fdao_gws_override, get_request_with_user



@override_settings(USERSERVICE_VALIDATION_MODULE=
                   "myuw.authorization.validate_netid",
                   USERSERVICE_OVERRIDE_AUTH_MODULE=
                   "myuw.authorization.can_override_user",
                   RESTCLIENTS_ADMIN_AUTH_MODULE=
                   "myuw.authorization.can_proxy_restclient")
@fdao_gws_override
class TestAdminDao(TestCase):

    def test_is_admin(self):
        get_request_with_user("javerage")
        self.assertEqual(get_netid_of_original_user(), "javerage")
        self.assertTrue(is_admin())
        self.assertTrue(can_override())

    def test_can_override(self):
        get_request_with_user("faculty")
        self.assertFalse(is_admin())
        self.assertTrue(can_override())

    def test_not_both(self):
        get_request_with_user("none")
        self.assertFalse(is_admin())
        self.assertFalse(can_override())

    def test_except(self):
        get_request_with_user("jerror")
        self.assertFalse(is_admin())
        self.assertFalse(can_override())
