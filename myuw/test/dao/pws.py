from django.test import TestCase
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidNetID
from restclients.pws import PWS


class TestPwsDao(TestCase):

    def test_not_in_pws_netid(self):
        self.assertRaises(InvalidNetID,
                          PWS().get_person_by_netid,
                          "notarealnetid")

    def test_pws_err(self):
        self.assertRaises(DataFailureException,
                          PWS().get_person_by_netid,
                          "nomockid")
