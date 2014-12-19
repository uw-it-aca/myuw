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
class TestLibrary(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_books(self):
        url = reverse("myuw_library_api")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["next_due"], "2014-05-27")
        self.assertEquals(data["holds_ready"], 1)
        self.assertEquals(data["fines"], 0)
        self.assertEquals(data["items_loaned"], 1)

    def test_invalid_books(self):
        url = reverse("myuw_library_api")
        get_user('nouser')
        self.client.login(username='nouser', password=get_user_pass('nouser'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
