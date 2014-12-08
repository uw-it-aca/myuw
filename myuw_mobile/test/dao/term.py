from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory

from datetime import datetime

from myuw_mobile.dao.term import _get_term_by_year_and_quarter, is_past
from myuw_mobile.dao.term import is_using_file_dao, get_default_date
from myuw_mobile.dao.term import get_comparison_date, get_current_quarter
from myuw_mobile.dao.term import get_next_quarter

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

    def test_default_date(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            date = get_default_date()
            self.assertEquals(date.year, 2013)
            self.assertEquals(date.month, 4)
            self.assertEquals(date.day, 15)

        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.Live'):
            now = datetime.now()
            date = get_default_date()
            self.assertEquals(date.year, now.year)
            self.assertEquals(date.month, now.month)
            self.assertEquals(date.day, now.day)


    def test_is_using_file_dao(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            self.assertTrue(is_using_file_dao())

        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.Live'):
            self.assertFalse(is_using_file_dao())

    def test_comparison_date(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            no_override = get_comparison_date(now_request)
            self.assertEquals(no_override.year, 2013)
            self.assertEquals(no_override.month, 4)
            self.assertEquals(no_override.day, 15)

            now_request.session["myuw_override_date"] = "2014-01-01"
            no_override = get_comparison_date(now_request)
            self.assertEquals(no_override.year, 2014)
            self.assertEquals(no_override.month, 1)
            self.assertEquals(no_override.day, 1)


    def test_current_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}

            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request.session["myuw_override_date"] = "2013-04-01"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request.session["myuw_override_date"] = "2013-03-31"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'winter')

            now_request.session["myuw_override_date"] = "2013-06-24"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request.session["myuw_override_date"] = "2013-06-23"
            quarter = get_current_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')


    def test_next_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            now_request = RequestFactory().get("/")
            now_request.session = {}

            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request.session["myuw_override_date"] = "2013-04-01"
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')

            now_request.session["myuw_override_date"] = "2013-03-31"
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'spring')

            now_request.session["myuw_override_date"] = "2013-06-24"
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'autumn')

            now_request.session["myuw_override_date"] = "2013-06-23"
            quarter = get_next_quarter(now_request)
            self.assertEquals(quarter.year, 2013)
            self.assertEquals(quarter.quarter, 'summer')
