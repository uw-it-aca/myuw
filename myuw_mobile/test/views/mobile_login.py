from django.test import TestCase
from django.conf import settings
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
class TestLoginRedirects(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage(self):
        url = reverse("myuw_login")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        response = self.client.get(url)

        valid_url = "http://testserver%s" % reverse("myuw_home")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), valid_url)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    # Putting this here to remove it, to make sure we're testing the default
    @override_settings(MYUW_USER_SERVLET_URL="http://some-test-server/myuw")
    def test_random_non_student(self):
        del settings.MYUW_USER_SERVLET_URL
        url = reverse("myuw_login")
        get_user('random')
        self.client.login(username='random', password=get_user_pass('random'))
        response = self.client.get(url)

        # This is the default...
        valid_url = "https://myuw.washington.edu/servlet/user"
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), valid_url)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    @override_settings(MYUW_USER_SERVLET_URL="http://some-test-server/myuw")
    def test_settings_url(self):
        url = reverse("myuw_login")
        get_user('random')
        self.client.login(username='random', password=get_user_pass('random'))
        response = self.client.get(url)

        # This is the default...
        valid_url = "http://some-test-server/myuw"
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), valid_url)
