from django.test import TestCase
from django.conf import settings

from myuw_mobile.dao.term import _get_term_by_year_and_quarter, is_past

from restclients.models import ClassSchedule, Term, Section, Person

class TestTerm(TestCase):

    def test_get_term(self):
        with self.settings(
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):

            term = _get_term_by_year_and_quarter(2013, "summer")
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, "summer")
            self.assertTrue(is_past(term))

            
    def test_is_past(self):
        with self.settings(
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):

            term = _get_term_by_year_and_quarter(2014, "winter")
            self.assertEqual(term.year, 2014)
            self.assertEqual(term.quarter, "winter")
            self.assertTrue(is_past(term))

