from django.test import TestCase
from django.conf import settings
from django.core.management import call_command


class TestClearSessions(TestCase):

    def test_run(self):
        with self.settings(DEL_SESSION_NUM=10):
            call_command('clear_expired_sessions')

    def test_run_default_limt(self):
        call_command('clear_expired_sessions')
