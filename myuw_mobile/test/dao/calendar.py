from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
import json

from datetime import date, datetime
from myuw_mobile.dao.calendar import get_events, _get_date


class TestCalendar(TestCase):
    def test_far_future(self):
        now = date(2013, 04, 15)
        cal = {'far_future': None}
        event_response = get_events(cal, now)
        self.assertEqual(len(event_response['future_active_cals']), 0)
        self.assertEqual(len(event_response['events']), 0)

    def test_past_events(self):
        now = date(2013, 04, 15)
        cal = {'past': None}
        event_response = get_events(cal, now)
        self.assertEqual(len(event_response['future_active_cals']), 0)
        self.assertEqual(len(event_response['events']), 0)

    def test_future(self):
        now = date(2013, 04, 15)
        cal = {'future_1': None}
        event_response = get_events(cal, now)
        self.assertEqual(len(event_response['future_active_cals']), 1)
        self.assertEqual(len(event_response['events']), 0)


    def test_future_two(self):
        now = date(2013, 04, 15)
        cal = {'future_1': None,
               'future_2': None}
        event_response = get_events(cal, now)
        self.assertTrue(True)
        self.assertEqual(len(event_response['future_active_cals']), 2)
        self.assertEqual(len(event_response['events']), 0)
        self.assertEqual(event_response['future_active_cals'][0]['count'], 1)
        self.assertEqual(event_response['future_active_cals'][1]['count'], 2)

    def test_current(self):
        now = date(2013, 04, 15)
        cal = {'5_current': None}
        event_response = get_events(cal, now)
        self.assertEqual(len(event_response['future_active_cals']), 0)
        self.assertEqual(len(event_response['events']), 5)

    def test_event_url(self):
        now = date(2013, 04, 15)

        cal = {'5_current': None}
        event_response = get_events(cal, now)
        self.assertEqual(event_response['events'][0]['event_url'],
                         'http://www.trumba.com/calendar/5_current?trumbaEmbed=view%%3Devent%%26eventid%%3D1107241160')
        cal = {'5_current': 'http://art.uw.edu/calendar'}
        event_response = get_events(cal, now)
        self.assertEqual(event_response['events'][0]['event_url'],
                         'http://art.uw.edu/calendar?trumbaEmbed=view%%3Devent%%26eventid%%3D1107241160')

    def test_date_sort(self):
        now = date(2013, 04, 15)
        cal = {'5_current': None}
        event_response = get_events(cal, now)
        self.assertEqual(event_response['events'][0]['summary'], 'Multi Day Event')
        self.assertEqual(event_response['events'][4]['summary'], 'Organic Chemistry Seminar: Prof. Matthew Becker4')

    def test_active_cals(self):
        now = date(2013, 04, 15)
        cal = {'5_current': None}
        event_response = get_events(cal, now)
        self.assertEqual(len(event_response['active_cals']), 1)
        self.assertEqual(event_response['active_cals'][0]['url'], "http://www.trumba.com/calendar/5_current")
        self.assertEqual(event_response['active_cals'][0]['title'], "Department of Five Events")

    def test_get_date(self):
        d = date(2013, 04, 15)
        dt = datetime(2013, 04, 15)
        self.assertEqual(_get_date(d), d)
        self.assertEqual(_get_date(dt), d)
