from django.test import TestCase
from django.conf import settings
from myuw.dao.affiliation import get_all_affiliations
from myuw.test import FDAO_SWS, FDAO_PWS,\
    get_request_with_date, get_request_with_user


class TestAffilliations(TestCase):
    def setUp(self):
        get_request_with_user('javerage')

    def test_eos_enrollment(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = get_request_with_user('jeos')
            affiliations = get_all_affiliations(now_request)

    def test_fyp_enrollment(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = get_request_with_user('javerage')
            affiliations = get_all_affiliations(now_request)
            self.assertTrue(affiliations['fyp'])
