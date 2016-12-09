from django.test import TestCase
from django.conf import settings
from myuw.dao.affiliation import get_all_affiliations
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestAffilliations(TestCase):
    def setUp(self):
        get_request()

    def test_eos_enrollment(self):
        now_request = get_request_with_user('jeos')
        affiliations = get_all_affiliations(now_request)

    def test_fyp_enrollment(self):
        now_request = get_request_with_user('javerage')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['fyp'])
