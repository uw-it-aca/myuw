from django.test import TransactionTestCase
from myuw.dao import get_netid_of_current_user, get_netid_of_original_user,\
    is_using_file_dao, is_thrive_viewer
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
