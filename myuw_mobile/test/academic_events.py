from django.test import TestCase
from myuw_mobile.views.api.academic_events import AcademicEvents
from icalendar import Calendar, Event
from datetime import datetime, date
from django.test.client import RequestFactory

class TestAcademicEvents(TestCase):
    def test_parsers(self):
        obj = AcademicEvents()

        cal = Calendar()
        event = Event()

        event.add('dtstart', date(2014, 12, 5))
        event.add('dtend', date(2014, 12, 6))
        event['summary'] = "Test Event"

        start, end = obj.parse_dates(event)

        self.assertEquals(start, "2014-12-05")
        self.assertEquals(end, "2014-12-06")

        year, quarter = obj.parse_year_quarter(event)
        self.assertEquals(year, None)
        self.assertEquals(quarter, None)

        event['description'] = '  Year: 2018 '
        year, quarter = obj.parse_year_quarter(event)
        self.assertEquals(year, '2018')
        self.assertEquals(quarter, None)

        event['description'] = '  Year: 2018\nQuarter: Winter\nMore Content'
        year, quarter = obj.parse_year_quarter(event)
        self.assertEquals(year, '2018')
        self.assertEquals(quarter, 'Winter')

    def test_filter_past(self):
        request = RequestFactory().get("/")
        request.session = {}
        request.session["myuw_override_date"] = "2011-01-01"

        past = Event()
        past.add('dtstart', date(2010, 01, 01))
        past.add('dtend', date(2010, 12, 31))
        past['summary'] = "Past Event"

        events = AcademicEvents().filter_past_events(request, [past])
        self.assertEquals(len(events), 0)

        request.session["myuw_override_date"] = "2010-12-31"
        events = AcademicEvents().filter_past_events(request, [past])
        self.assertEquals(len(events), 1)

    def test_filter_future(self):
        request = RequestFactory().get("/")
        request.session = {}
        request.session["myuw_override_date"] = "2012-12-01"

        past = Event()
        past.add('dtstart', date(2014, 01, 01))
        past.add('dtend', date(2014, 12, 31))
        past['summary'] = "Future Event"

        events = AcademicEvents().filter_too_future_events(request, [past])
        self.assertEquals(len(events), 0)

        request.session["myuw_override_date"] = "2013-01-01"
        events = AcademicEvents().filter_too_future_events(request, [past])
        self.assertEquals(len(events), 1)
