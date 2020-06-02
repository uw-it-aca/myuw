from django.test import TransactionTestCase
from django.core.management import call_command
from django.contrib.sessions.models import Session
from django.utils import timezone


class TestDeleteSessions(TransactionTestCase):

    def test_run(self):
        session_data = Session.get_session_store_class()().encode(
            {'_auth_user_id': '287',
             '_auth_user_backend': 'RemoteUserBackend',
             '_auth_user_hash': 'ac3a44eea77b1680df',
             '_session_expiry': 601,
             'uw_oidc_idtoken': 'eyJr..XdQ',
             '_uw_original_user': 'javerage'})
        Session.objects.create(session_key="a",
                               session_data=session_data,
                               expire_date=timezone.now())
        session_data1 = Session.get_session_store_class()().encode(
            {'_auth_user_id': '287',
             '_session_expiry': 601,
             'uw_oidc_idtoken': 'eyJr..XdQ',
             '_uw_original_user': 'javerage'})
        Session.objects.create(session_key="b",
                               session_data=session_data1,
                               expire_date=timezone.now())
        self.assertEqual(Session.objects.all().count(), 2)
        call_command('del_token_session', 'javerage')
        self.assertEqual(Session.objects.all().count(), 0)
