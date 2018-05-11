from django.conf import settings
from django.test import TransactionTestCase
from django.test.client import RequestFactory
from userservice.user import UserServiceMiddleware
from userservice.user import UserService
from myuw.dao import get_netid_of_current_user, get_netid_of_original_user,\
    is_using_file_dao, is_thrive_viewer, not_overriding
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestDaoInit(TransactionTestCase):

    def test_get_netid_of_current_user(self):
        req = get_request_with_user("javerage")
        netid = get_netid_of_current_user(req)
        self.assertEqual(netid, "javerage")

    def test_get_netid_of_original_user(self):
        netid = get_netid_of_original_user()
        self.assertEqual(netid, "javerage")

    def test_is_using_file_dao(self):
        self.assertTrue(is_using_file_dao())

    def test_is_thrive_viewer(self):
        self.assertTrue(is_thrive_viewer("jnew", "fyp"))
        self.assertTrue(is_thrive_viewer("javg001", "au_xfer"))
        self.assertTrue(is_thrive_viewer("javg002", "wi_xfer"))

    def test_overriding(self):
        with self.settings(MYUW_SAVE_USER_ACTIONS_WHEN_OVERRIDE=False):
            self.assertFalse(not_overriding())
            # set override
            request = RequestFactory().get("/")
            request.session = {}
            request.session["_us_override_user"] = 'bill'
            UserServiceMiddleware().process_request(request)
            self.assertFalse(not_overriding())

    def test_ignore_overriding(self):
        with self.settings(MYUW_SAVE_USER_ACTIONS_WHEN_OVERRIDE=True):
            self.assertTrue(not_overriding())
            request = RequestFactory().get("/")
            request.session = {}
            request.session["_us_override_user"] = 'bill'
            UserServiceMiddleware().process_request(request)
            self.assertTrue(not_overriding())
