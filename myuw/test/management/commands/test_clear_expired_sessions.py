from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError

class TestClearSessions(TestCase):

    def test_run(self):
        try:
            call_command('clear_expired_sessions')
        except CommandError as err:
            self.assertFalse(str(err))
