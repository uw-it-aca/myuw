from django.test import TransactionTestCase
from django.test.client import RequestFactory
from userservice.user import UserServiceMiddleware, UserService
from myuw.dao import get_netid_of_current_user, get_netid_of_original_user,\
    is_using_file_dao, is_thrive_viewer, is_action_disabled,\
    is_hx_toolkit_viewer
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user, set_override_user
from myuw.test.api import MyuwApiTest


@fdao_pws_override
@fdao_sws_override
class TestDaoInit(MyuwApiTest):

    def test_get_netid_of_current_user(self):
        req = get_request_with_user("javerage")
        netid = get_netid_of_current_user()
        self.assertEqual(netid, "javerage")

        netid = get_netid_of_current_user(req)
        self.assertEqual(netid, "javerage")

    def test_get_netid_of_original_user(self):
        netid = get_netid_of_original_user()
        self.assertEqual(netid, "javerage")

    def test_is_using_file_dao(self):
        self.assertTrue(is_using_file_dao())

    def test_is_hx_toolkit_viewer(self):
        request = get_request_with_user("staff")
        self.assertTrue(is_hx_toolkit_viewer(request))

    def test_is_thrive_viewer(self):
        self.assertTrue(is_thrive_viewer("jnew", "fyp"))
        self.assertTrue(is_thrive_viewer("javg001", "au_xfer"))
        self.assertTrue(is_thrive_viewer("javg002", "wi_xfer"))

    def test_is_action_disabled(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True):
            request = get_request_with_user('javerage')
            self.assertEquals(UserService().get_original_user(), 'javerage')
            self.assertEquals(UserService().get_override_user(), None)
            self.assertFalse(is_action_disabled())

            set_override_user('bill')
            self.assertEquals(UserService().get_original_user(), 'javerage')
            self.assertEquals(UserService().get_override_user(), 'bill')
            self.assertTrue(is_action_disabled())

    def test_action_not_disabled(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=False):
            request = get_request_with_user('javerage')
            self.assertFalse(is_action_disabled())

            set_override_user('bill')
            self.assertEquals(UserService().get_original_user(), 'javerage')
            self.assertEquals(UserService().get_override_user(), 'bill')
            self.assertFalse(is_action_disabled())
