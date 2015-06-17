from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
import json


FDAO_SWS = 'restclients.dao_implementation.sws.File'
Session = 'django.contrib.sessions.middleware.SessionMiddleware'
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
RemoteUser = 'django.contrib.auth.middleware.RemoteUserMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'


@override_settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                   MIDDLEWARE_CLASSES=(Session,
                                       Common,
                                       CsrfView,
                                       Auth,
                                       RemoteUser,
                                       Message,
                                       XFrame,
                                       UserService,
                                       ),
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND,)
                   )
class TestNotices(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_books(self):
        url = reverse("myuw_notices_api")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 7)
        self.assertEquals(data[0]["is_read"], False)

        hash_value = data[0]["id_hash"]

        response = self.client.put(
            url,
            data='{"notice_hashes":["%s"]}' % hash_value)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '')

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 6)

        match = False
        for el in data:
            if el["id_hash"] == hash_value:
                match = True
                self.assertEquals(el["is_read"], True)

        self.assertEquals(match, True)

        response = self.client.put(
            url, data='{"notice_hashes":["fake-fake-fake"]}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '')
