from django.test import TestCase
from django.conf import settings
from restclients.models import ClassSchedule, Term, Section, Person
from myuw_mobile.dao.term import _get_term_by_year_and_quarter
from myuw_mobile.dao.schedule import _get_schedule
from myuw_mobile.dao.registered_term import _get_registered_summer_terms,\
    _must_displayed_separately, _get_registered_future_quarters


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestRegisteredTerm(TestCase):

    def test_get_registered_summer_terms(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = _get_term_by_year_and_quarter(2013, "summer")
            schedule = _get_schedule(regid, term)
            data = _get_registered_summer_terms(schedule.sections)
            self.assertTrue(data["B"])
            self.assertTrue(data["A"])

    def test_must_displayed_separately(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = _get_term_by_year_and_quarter(2013, "summer")
            schedule = _get_schedule(regid, term)
            self.assertTrue(_must_displayed_separately(schedule))

    def test_get_registered_future_quarters(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term1 = _get_term_by_year_and_quarter(2013, "summer")
            schedule1 = _get_schedule(regid, term1)
            self.assertEqual(len(schedule1.sections), 3)

            term2 = _get_term_by_year_and_quarter(2013, "autumn")
            schedule2 = _get_schedule(regid, term2)
            self.assertEqual(len(schedule2.sections), 1)

            terms = _get_registered_future_quarters(schedule1, schedule2)
            self.assertTrue(len(terms) == 3)
            self.assertTrue(terms[0]['year'] == 2013)
            self.assertEqual(terms[0]['quarter'], "Summer")
            self.assertEqual(terms[0]['summer_term'], "a-term")

            self.assertTrue(terms[1]['year'] == 2013)
            self.assertEqual(terms[1]['quarter'], "Summer")
            self.assertEqual(terms[1]['summer_term'], "b-term")

            self.assertTrue(terms[2]['year'] == 2013)
            self.assertEqual(terms[2]['quarter'], "Autumn")
            self.assertEqual(terms[2]['summer_term'], "")

            terms = _get_registered_future_quarters(None, None)
            self.assertEqual(len(terms), 0)
