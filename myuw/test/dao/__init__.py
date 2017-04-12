from django.test import TestCase
from django.conf import settings
from myuw.dao import is_seru_viewer
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestNetidInList(TestCase):
    def setUp(self):
        get_request()


    def test_seru_viewer(self):
        is_seru = is_seru_viewer('javerage')
        self.assertTrue(is_seru)

        is_seru = is_seru_viewer('jtacoma')
        self.assertFalse(is_seru)
