from datetime import timedelta
from django.test import TransactionTestCase
from django.core.management import call_command
from django.contrib.sessions.models import Session
from django.utils import timezone
from myuw.util.sessions import delete_sessions, SCOPE_ALL, SCOPE_IDTOKEN


class TestDeleteSessions(TransactionTestCase):

    def test_run(self):
        session_data = Session.get_session_store_class()().encode(
            {'_auth_user_id': '1',
             '_auth_user_backend': 'RemoteUserBackend',
             '_auth_user_hash': 'ac3a44eea77b1680df',
             '_session_expiry': 600,
             'uw_oidc_idtoken': 'eyJr..XdQ',
             '_uw_original_user': 'javerage'})
        Session.objects.create(session_key="a",
                               session_data=session_data,
                               expire_date=(timezone.now() +
                                            timedelta(seconds=600)))
        session_data1 = Session.get_session_store_class()().encode(
            {'_auth_user_id': '2',
             '_auth_user_backend': 'RemoteUserBackend',
             '_auth_user_hash': 'ac3a44eea77b1680dg',
             '_session_expiry': 600,
             '_us_original_user': 'javerage'})
        Session.objects.create(session_key="b",
                               session_data=session_data1,
                               expire_date=(timezone.now() +
                                            timedelta(seconds=600)))
        session_data2 = Session.get_session_store_class()().encode(
            {'_auth_user_id': '3',
             '_auth_user_backend': 'RemoteUserBackend',
             '_auth_user_hash': 'ac3a44eea77b1680dg'})
        Session.objects.create(session_key="c",
                               session_data=session_data2,
                               expire_date=(timezone.now() +
                                            timedelta(seconds=600)))
        self.assertEqual(Session.objects.all().count(), 3)

        delete_sessions('javerage', SCOPE_IDTOKEN)
        self.assertEqual(Session.objects.all().count(), 2)
        delete_sessions('javerage', SCOPE_ALL)
        self.assertEqual(Session.objects.all().count(), 1)
        delete_sessions('javerage', "")
        self.assertEqual(Session.objects.all().count(), 1)
