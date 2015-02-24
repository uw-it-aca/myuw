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
    def test_get_events(self):
        now = date(2013, 04, 15)
        cal = {'organic': None}
        event_response = get_events([cal], now)
        self.assertEqual(len(event_response['active_cals']), 0)
        self.assertEqual(len(event_response['events']), 4)


    def test_past_30(self):
        now = date(2013, 04, 15)
        cal = {'past30d': None}
        event_response = get_events([cal], now)
        self.assertEqual(len(event_response['active_cals']), 0)
        self.assertEqual(len(event_response['events']), 0)


    def test_active(self):
        now = date(2013, 04, 15)
        cal = {'within30d': None}
        event_response = get_events([cal], now)
        print event_response
        self.assertTrue('within30d' in event_response['active_cals'])
        self.assertEqual(event_response['active_cals']['within30d']['count'], 5)
        self.assertEqual(len(event_response['events']), 0)