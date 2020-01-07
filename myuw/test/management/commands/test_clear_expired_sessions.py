from django.test import TestCase
from django.core.management import call_command


class TestClearSessions(TestCase):

    def test_run(self):
        call_command('clear_expired_sessions')
