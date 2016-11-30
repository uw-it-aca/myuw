from django.test import TestCase
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidNetID
from restclients.pws import PWS
from myuw.dao.pws import get_display_name_of_current_user
from myuw.test import FDAO_SWS, FDAO_PWS, get_request_with_user


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
            get_request_with_user('javerage')
            name = get_display_name_of_current_user()
            self.assertEqual(name, 'J. Average Student')
