from django.test import TransactionTestCase
from django.core.management import call_command
from django.contrib.sessions.models import Session
from django.utils import timezone


class TestDeleteSessions(TransactionTestCase):

    def test_run(self):
        call_command('del_token_session', 'javerage')
