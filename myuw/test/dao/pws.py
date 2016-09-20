from django.test import TestCase
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidNetID
from restclients.pws import PWS
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from myuw.dao.pws import get_display_name_of_current_user
from userservice.user import UserServiceMiddleware


FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestPwsDao(TestCase):

    def test_not_in_pws_netid(self):
        self.assertRaises(InvalidNetID,
                          PWS().get_person_by_netid,
                          "thisisnotarealnetid")

    def test_pws_err(self):
        self.assertRaises(DataFailureException,
                          PWS().get_person_by_netid,
                          "nomockid")

    def test_display_name(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-09-20"
            user = User.objects.create_user(username='javerage',
                                            email='none@example.com',
                                            password='')
            now_request.user = user
            UserServiceMiddleware().process_request(now_request)
            name = get_display_name_of_current_user()
            self.assertEqual(name, 'J. Average Student')
