from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from myuw.dao.affiliation import get_all_affiliations
from userservice.user import UserServiceMiddleware


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
