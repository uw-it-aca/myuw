from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from restclients.models import ClassSchedule, Term, Section, Person
from myuw.dao.term import get_specific_term
from myuw.dao.schedule import _get_schedule
from myuw.dao.registered_term import _get_registered_summer_terms,\
    _must_displayed_separately, _get_registered_future_quarters


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestRegisteredTerm(TestCase):

    def test_get_registered_summer_terms(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = get_specific_term(2013, "summer")
            schedule = _get_schedule(regid, term)
            data = _get_registered_summer_terms(schedule.sections)
            self.assertTrue(data["B"])
            self.assertTrue(data["A"])

    def test_must_displayed_separately(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = get_specific_term(2013, "summer")
            schedule = _get_schedule(regid, term)
            self.assertTrue(_must_displayed_separately(schedule))

    def test_get_registered_future_quarters(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):

            now_request = RequestFactory().get("/")
            now_request.session = {}

            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term1 = get_specific_term(2013, "summer")
            schedule1 = _get_schedule(regid, term1)
            self.assertEqual(len(schedule1.sections), 3)

            term2 = get_specific_term(2013, "autumn")
            schedule2 = _get_schedule(regid, term2)
            self.assertEqual(len(schedule2.sections), 1)

            terms = _get_registered_future_quarters(now_request, schedule1,
                                                    schedule2)
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

            terms = _get_registered_future_quarters(now_request, None, None)
            self.assertEqual(len(terms), 0)

            # MUWM-3010
            # Baseline pre-summer
            now_request.session["myuw_override_date"] = "2013-04-01"

            terms = _get_registered_future_quarters(now_request, schedule1,
                                                    schedule2)
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

            # Summer has started - so no a-term
            now_request.session["myuw_override_date"] = "2013-06-30"
            terms = _get_registered_future_quarters(now_request, schedule1,
                                                    schedule2)
            self.assertTrue(len(terms) == 2)

            self.assertTrue(terms[0]['year'] == 2013)
            self.assertEqual(terms[0]['quarter'], "Summer")
            self.assertEqual(terms[0]['summer_term'], "b-term")

            self.assertTrue(terms[1]['year'] == 2013)
            self.assertEqual(terms[1]['quarter'], "Autumn")
            self.assertEqual(terms[1]['summer_term'], "")

            # Summer b-term has started - so no a-term or b-term
            now_request.session["myuw_override_date"] = "2013-07-30"
            terms = _get_registered_future_quarters(now_request, schedule1,
                                                    schedule2)
            self.assertTrue(len(terms) == 1)

            self.assertTrue(terms[0]['year'] == 2013)
            self.assertEqual(terms[0]['quarter'], "Autumn")
            self.assertEqual(terms[0]['summer_term'], "")
