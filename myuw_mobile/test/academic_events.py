from django.test import TestCase
from myuw_mobile.views.api.academic_events import AcademicEvents
from icalendar import Calendar, Event
from datetime import datetime, date

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

