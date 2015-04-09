from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
import json
import pytz

from datetime import date, datetime
from myuw_mobile.dao.calendar import get_events


class TestCalendar(TestCase):
    def setUp(self):
        self.now = datetime(2013, 04, 15, 0, 0, 0, tzinfo=pytz.utc)

    def test_far_future(self):
        cal = {'far_future': None}
        event_response = get_events(cal, self.now)
        self.assertEqual(len(event_response['future_active_cals']), 0)
        self.assertEqual(len(event_response['events']), 0)

    def test_past_events(self):
        cal = {'past': None}
        event_response = get_events(cal, self.now)
        self.assertEqual(len(event_response['future_active_cals']), 0)
        self.assertEqual(len(event_response['events']), 0)

    def test_future(self):
        cal = {'future_1': None}
        event_response = get_events(cal, self.now)
        self.assertEqual(len(event_response['future_active_cals']), 1)
        self.assertEqual(len(event_response['events']), 0)

    def test_future_two(self):
        cal = {'future_1': None,
               'future_2': None}
        event_response = get_events(cal, self.now)
        self.assertTrue(True)
        self.assertEqual(len(event_response['future_active_cals']), 2)
        self.assertEqual(len(event_response['events']), 0)
        self.assertEqual(event_response['future_active_cals'][0]['count'], 1)
        self.assertEqual(event_response['future_active_cals'][1]['count'], 2)

    def test_current(self):
        cal = {'5_current': None}
        event_response = get_events(cal, self.now)
        self.assertEqual(len(event_response['future_active_cals']), 0)
        self.assertEqual(len(event_response['events']), 5)

    def test_event_url(self):
        cal = {'5_current': None}
        event_response = get_events(cal, self.now)
        self.assertEqual(event_response['events'][0]['event_url'],
                         'http://www.trumba.com/calendar/5_current?trumbaEmbed=eventid%3D1107241160%26view%3Devent')

    def test_date_sort(self):
        cal = {'5_current': None}
        event_response = get_events(cal, self.now)
        self.assertEqual(event_response['events'][0]['summary'], 'Multi Day Event')
        self.assertEqual(event_response['events'][4]['summary'], 'Organic Chemistry Seminar: Prof. Matthew Becker4')

    def test_active_cals(self):
        cal = {'5_current': None}
        event_response = get_events(cal, self.now)
        self.assertEqual(len(event_response['active_cals']), 1)
        self.assertEqual(event_response['active_cals'][0]['url'], "http://www.trumba.com/calendar/5_current")
        self.assertEqual(event_response['active_cals'][0]['title'], "Department of Five Events")

    def test_all_day(self):
        cal = {'5_current': None}
        event_response = get_events(cal, self.now)
        self.assertTrue(event_response['events'][3]['is_all_day'])

    def test_no_location(self):
        cal = {'5_current': None}
        event_response = get_events(cal, self.now)
        self.assertEqual(event_response['events'][3]['event_location'], "")

    def test_all_day(self):
        cal = {'5_current': None}
        event_response = get_events(cal, self.now)
        self.assertTrue(event_response['events'][3]['is_all_day'])
        self.assertFalse(event_response['events'][2]['is_all_day'])

        self.assertEqual(event_response['events'][3]['end'], '2013-04-18')
