from django.test import TestCase
from myuw.dao import is_using_file_dao


FDAO_SWS = 'restclients.dao_implementation.sws.File'
LDAO_SWS = 'restclients.dao_implementation.sws.Live'


class TestDao(TestCase):
    def test_is_using_file_dao(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertTrue(is_using_file_dao())

        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=LDAO_SWS):
            self.assertFalse(is_using_file_dao())
