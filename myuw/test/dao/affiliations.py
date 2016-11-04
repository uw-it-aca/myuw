from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from myuw.dao.affiliation import get_all_affiliations, valid_myuw_user
from userservice.user import UserServiceMiddleware
from myuw.dao.exceptions import UnsupportedAffiliationException


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestAffilliations(TestCase):
    def test_eos_enrollment(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}

            user = User.objects.create_user(username='jeos',
                                            email='jeos@example.com',
                                            password='')

            now_request.user = user
            UserServiceMiddleware().process_request(now_request)
            affiliations = get_all_affiliations(now_request)

    def test_fyp_enrollment(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}

            user = User.objects.create_user(username='javerage',
                                            email='javerage@example.com',
                                            password='')

            now_request.user = user
            UserServiceMiddleware().process_request(now_request)
            affiliations = get_all_affiliations(now_request)
            self.assertTrue(affiliations['fyp'])

    def test_valid_myuw_user(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            user = User.objects.create_user(username='javerage',
                                            email='javerage@example.com',
                                            password='')

            now_request.user = user
            UserServiceMiddleware().process_request(now_request)
            try:
                valid_myuw_user(now_request, False)
            except UnsupportedAffiliationException:
                self.fail('valid_myuw_user raised exception')

    def test_invalid_myuw_user(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            user = User.objects.create_user(username='none6',
                                            email='none6@example.com',
                                            password='')

            now_request.user = user
            UserServiceMiddleware().process_request(now_request)
            with self.assertRaises(UnsupportedAffiliationException):
                valid_myuw_user(now_request, False)
