from django.test import TestCase
from myuw_mobile.dao.schedule import _get_schedule
from restclients.models import Term
from myuw_mobile.dao.textbook import get_textbook_by_schedule, \
    get_verba_link_by_schedule


class TestTextbooks(TestCase):
    def test_get_by_schedule(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2012
        term.quarter = "summer"
        schedule = _get_schedule(regid, term)

        books = get_textbook_by_schedule(schedule)
        self.assertEquals(len(books), 5)
        self.assertEquals(books["13833"][0].title,
                          "Quantum Chemistry (6th Edition)")
        self.assertEquals(get_textbook_by_schedule(None), None)

    def test_get_verba_by_schedule(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2012
        term.quarter = "summer"
        schedule = _get_schedule(regid, term)

        expected_link = ("http://uw-seattle.verbacompare.com/m?"
                         "section_id=AB12345&quarter=summer")
        returned_link = get_verba_link_by_schedule(schedule)
        self.assertEquals(returned_link, expected_link)

        returned_link = get_verba_link_by_schedule(None)
        self.assertEquals(returned_link, None)
