from django.test import TestCase
from django.conf import settings
from myuw.dao import _is_optin_user
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestNetidInList(TestCase):
    def test_optin_user(self):
        is_optin = _is_optin_user('javerage')
        self.assertTrue(is_optin)

        not_optin = _is_optin_user('jtacoma')
        self.assertFalse(not_optin)
