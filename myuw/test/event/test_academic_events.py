# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.views.api.academic_events import AcademicEvents
from icalendar import Calendar, Event
from datetime import datetime, date
from myuw.test import get_request_with_date


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
        self.assertEquals(end, "2014-12-05")

        event['X-TRUMBA-CUSTOMFIELD'] = [
            'Important Dates/Deadlines',
            'xxx xx xx']
        year, quarter = obj.parse_year_quarter(event)
        self.assertEquals(year, None)
        self.assertEquals(quarter, None)

        event['X-TRUMBA-CUSTOMFIELD'] = [
            'Important Dates/Deadlines',
            '2013',
            'Spring']
        year, quarter = obj.parse_year_quarter(event)
        self.assertEquals(year, '2013')
        self.assertEquals(quarter, 'Spring')

    def test_categorize_event(self):
        event = Event()
        categories = AcademicEvents().get_event_categories(event)
        self.assertEquals(categories, {
            'breaks': False,
            'classes': False,
            'grade': False,
            'registration': False,
            'term_breaks': False
        })

        event['categories'] = 'Holidays'
        categories = AcademicEvents().get_event_categories(event)
        self.assertEquals(categories, {
            'breaks': True,
            'classes': False,
            'grade': False,
            'registration': False,
            'term_breaks': False
        })

        event['categories'] = 'Dates of Instruction'
        event['summary'] = 'Quarter Break - Spring'
        categories = AcademicEvents().get_event_categories(event)
        self.assertEquals(categories, {
            'breaks': True,
            'classes': True,
            'grade': False,
            'registration': False,
            'term_breaks': True
        })

        event['categories'] = 'Registration dates'
        categories = AcademicEvents().get_event_categories(event)
        self.assertEquals(categories, {
            'breaks': False,
            'classes': False,
            'grade': False,
            'registration': True,
            'term_breaks': False
        })

        event['categories'] = 'Grade deadlines'
        categories = AcademicEvents().get_event_categories(event)
        self.assertEquals(categories, {
            'breaks': False,
            'classes': False,
            'grade': True,
            'registration': False,
            'term_breaks': False
        })

    def test_filter_past(self):
        request = get_request_with_date("2011-01-01")

        past = Event()
        past.add('dtstart', date(2010, 1, 1))
        past.add('dtend', date(2010, 12, 31))
        past['summary'] = "Past Event"

        events = AcademicEvents().filter_past_events(request, [past])
        self.assertEquals(len(events), 0)

        request = get_request_with_date("2010-12-30")
        events = AcademicEvents().filter_past_events(request, [past])
        self.assertEquals(len(events), 1)

    def test_filter_future(self):
        request = get_request_with_date("2012-12-01")

        past = Event()
        past.add('dtstart', date(2014, 1, 1))
        past.add('dtend', date(2014, 12, 31))
        past['summary'] = "Future Event"

        events = AcademicEvents().filter_too_future_events(request, [past])
        self.assertEquals(len(events), 0)

        request = get_request_with_date("2013-01-01")
        events = AcademicEvents().filter_too_future_events(request, [past])
        self.assertEquals(len(events), 1)

    def test_current_filter(self):
        request = get_request_with_date("2012-12-10")

        e1 = Event()
        e1.add('dtstart', date(2012, 12, 1))
        e1.add('dtend', date(2014, 12, 31))
        e1['summary'] = "Event 1"

        e2 = Event()
        e2.add('dtstart', date(2012, 12, 4))
        e2.add('dtend', date(2014, 12, 31))
        e2['summary'] = "Event 2"

        e3 = Event()
        e3.add('dtstart', date(2012, 12, 10))
        e3.add('dtend', date(2012, 12, 10))
        e3['summary'] = "Event 3"

        e4 = Event()
        e4.add('dtstart', date(2012, 12, 11))
        e4.add('dtend', date(2012, 12, 15))
        e4['summary'] = "Event 4"

        e5 = Event()
        e5.add('dtstart', date(2012, 12, 13))
        e5.add('dtend', date(2012, 12, 15))
        e5['summary'] = "Event 5"

        e6 = Event()
        e6.add('dtstart', date(2012, 12, 14))
        e6.add('dtend', date(2012, 12, 15))
        e6['summary'] = "Event 6"

        # Test that there are only events in the first 3 of the valid dates
        events = AcademicEvents().filter_non_current(
            request, [e1, e2, e3, e4, e5, e6])

        self.assertEquals(len(events), 5)
        self.assertEquals(events[0]['summary'], 'Event 1')
        self.assertEquals(events[1]['summary'], 'Event 2')
        self.assertEquals(events[2]['summary'], 'Event 3')
        self.assertEquals(events[3]['summary'], 'Event 4')
        self.assertEquals(events[4]['summary'], 'Event 5')

        e7 = Event()
        e7.add('dtstart', date(2013, 2, 13))
        e7.add('dtend', date(2013, 2, 15))
        e7['summary'] = "Event 7"

        e8 = Event()
        e8.add('dtstart', date(2013, 2, 13))
        e8.add('dtend', date(2013, 2, 15))
        e8['summary'] = "Event 8"

        e9 = Event()
        e9.add('dtstart', date(2013, 2, 14))
        e9.add('dtend', date(2013, 2, 15))
        e9['summary'] = "Event 9"

        # Test that both events outside of 4 weeks,
        # but on the first day outside are included
        events = AcademicEvents().filter_non_current(request, [e7, e8, e9])
        self.assertEquals(len(events), 2)
        self.assertEquals(events[0]['summary'], 'Event 7')
        self.assertEquals(events[1]['summary'], 'Event 8')

        # Make sure that just one event inside of
        # the 4 week span blocks everything outside
        events = AcademicEvents().filter_non_current(request, [e6, e7, e8, e9])
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0]['summary'], 'Event 6')
