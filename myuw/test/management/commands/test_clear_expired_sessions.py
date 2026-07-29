# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta

from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from myuw.management.commands.clear_expired_sessions import (
    get_cut_off_params,
)


class TestClearSessions(TestCase):

    def test_run(self):
        Session.objects.create(session_key="a",
                               session_data="a",
                               expire_date=timezone.now() - timedelta(days=1))
        call_command('clear_expired_sessions', 1)
        for i in range(10001):
            Session.objects.create(
                session_key=f"a{i}",
                session_data=f"a{i}",
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
