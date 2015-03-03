from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
import json

from datetime import date
from myuw_mobile.dao.calendar import get_events


class TestCalendar(TestCase):
    def test_far_future(self):
        now = date(2013, 04, 15)
        cal = {'far_future': None}
        event_response = get_events([cal], now)
        self.assertEqual(len(event_response['active_cals']), 0)
        self.assertEqual(len(event_response['events']), 0)

    def test_past_events(self):
        now = date(2013, 04, 15)
        cal = {'past': None}
        event_response = get_events([cal], now)
        self.assertEqual(len(event_response['active_cals']), 0)
        self.assertEqual(len(event_response['events']), 0)

    def test_future(self):
        now = date(2013, 04, 15)
        cal = {'future_1': None}
        event_response = get_events([cal], now)
        self.assertEqual(len(event_response['active_cals']), 1)
        self.assertEqual(len(event_response['events']), 0)

    def test_current(self):
        now = date(2013, 04, 15)
        cal = {'5_current': None}
        event_response = get_events([cal], now)
        self.assertEqual(len(event_response['active_cals']), 0)
        self.assertEqual(len(event_response['events']), 5)
