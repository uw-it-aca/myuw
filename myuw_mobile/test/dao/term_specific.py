from datetime import datetime
from django.test import TestCase
from django.conf import settings
from restclients.models.sws import ClassSchedule, Term, Section, Person
from myuw_mobile.dao.term.specific import get_eof_term_yq,\
    get_eof_last_instruction_yq, get_eof_term_after_yq,\
    get_first_day_term_after_yq


FDAO_SWS = 'restclients.dao_implementation.sws.File'
LDAO_SWS = 'restclients.dao_implementation.sws.Live'


class TestTermSpecific(TestCase):
    def test_get_eof_last_instruction_yq(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertEqual(get_eof_last_instruction_yq(2013,
                                                         "spring"),
                             datetime(2013, 6, 8, 0, 0, 0))
            self.assertEqual(get_eof_last_instruction_yq(2013,
                                                         "summer"),
                             datetime(2013, 8, 24, 0, 0, 0))

    def test_get_first_day_term_after_yq(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertEqual(get_first_day_term_after_yq(2012,
                                                         "autumn"),
                             datetime(2013, 1, 7, 0, 0, 0))
            self.assertEqual(get_first_day_term_after_yq(2013,
                                                         "spring"),
                             datetime(2013, 6, 24, 0, 0, 0))

    def test_get_eof_term_yq(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertEqual(get_eof_term_yq(2013, "autumn"),
                             datetime(2013, 12, 18, 0, 0, 0))
            self.assertEqual(get_eof_term_yq(2013, "summer"),
                             datetime(2013, 8, 28, 0, 0, 0))

    def test_get_eof_term_after_yq(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            self.assertEqual(get_eof_term_after_yq(2013, "summer"),
                             datetime(2013, 12, 18, 0, 0, 0))
            self.assertEqual(get_eof_term_after_yq(2013, "spring"),
                             datetime(2013, 8, 28, 0, 0, 0))
