from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from userservice.user import UserServiceMiddleware, UserService
from myuw.dao import get_netid_of_original_user
from myuw.dao.admin import is_admin, can_override
from myuw.test import fdao_gws_override, get_user
from myuw.test.api import standard_test_override


@fdao_gws_override
@standard_test_override
class TestAdminDao(TestCase):

    def set_user(self, username):
        request = RequestFactory().get("/")
        request.session = {}
        request.user = get_user(username)
        UserServiceMiddleware().process_request(request)

    def test_is_admin(self):
        self.set_user("javerage")
        self.assertEqual(get_netid_of_original_user(), "javerage")
        self.assertTrue(is_admin())
        self.assertTrue(can_override())

    def test_can_override(self):
        self.set_user("faculty")
        self.assertFalse(is_admin())
        self.assertTrue(can_override())

    def test_not_both(self):
        self.set_user("none")
        self.assertFalse(is_admin())
        self.assertFalse(can_override())

    def test_except(self):
        self.set_user("jerror")
        self.assertFalse(is_admin())
        self.assertFalse(can_override())
