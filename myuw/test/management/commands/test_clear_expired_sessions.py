from django.test import TestCase
from django.core.management import call_command
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta
from myuw.management.commands.clear_expired_sessions import (
    get_cut_off_params, run_delete)


class TestClearSessions(TestCase):

    def test_run(self):
        Session.objects.create(session_key="a",
                               session_data="a",
                               expire_date=timezone.now() - timedelta(days=1))
        call_command('clear_expired_sessions', 1)
        for i in range(0, 10001):
            Session.objects.create(
                session_key="a{}".format(i),
                session_data="a{}".format(i),
                expire_date=timezone.now() - timedelta(days=1))
        self.assertEqual(Session.objects.filter(
            expire_date__lt=timezone.now()).count(), 10001)
        call_command('clear_expired_sessions', 1)
        self.assertEqual(Session.objects.filter(
            expire_date__lt=timezone.now()).count(), 0)

    def test_get_cut_off_params(self):
        start_hr, inc_hrs = get_cut_off_params(49999)
        self.assertEqual(start_hr, 20)
        self.assertEqual(inc_hrs, -4)
        start_hr, inc_hrs = get_cut_off_params(99999)
        self.assertEqual(start_hr, 22)
        self.assertEqual(inc_hrs, -2)
        start_hr, inc_hrs = get_cut_off_params(200000)
        self.assertEqual(start_hr, 23)
        self.assertEqual(inc_hrs, -1)
