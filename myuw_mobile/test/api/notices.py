from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
import json

@override_settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                   MIDDLEWARE_CLASSES = (
                                'django.contrib.sessions.middleware.SessionMiddleware',
                                'django.middleware.common.CommonMiddleware',
                                'django.middleware.csrf.CsrfViewMiddleware',
                                'django.contrib.auth.middleware.AuthenticationMiddleware',
                                'django.contrib.auth.middleware.RemoteUserMiddleware',
                                'django.contrib.messages.middleware.MessageMiddleware',
                                'django.middleware.clickjacking.XFrameOptionsMiddleware',
                                'userservice.user.UserServiceMiddleware',
                                ),
                   AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
                   )
class TestNotices(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_books(self):
        url = reverse("myuw_notices_api")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 6)
        self.assertEquals(data[0]["is_read"], False)

        hash_value = data[0]["id_hash"]

        response = self.client.put(url, data='{"notice_hashes":["%s"]}' % hash_value)

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

        response = self.client.put(url, data='{"notice_hashes":["fake-fake-fake"]}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '')
