import json
from unittest2 import skipIf
from django.test.utils import override_settings
from django.test import TestCase
from django.conf import settings
from django.test.client import Client
from django.core.urlresolvers import reverse
from myuw_mobile.test.api import missing_url, get_user, get_user_pass


FDAO_SWS = 'restclients.dao_implementation.sws.File'
Session = 'django.contrib.sessions.middleware.SessionMiddleware',
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
RemoteUser = 'django.contrib.auth.middleware.RemoteUserMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'


@override_settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                   MIDDLEWARE_CLASSES=(SessionMiddleware
                                       Common,
                                       CsrfView,
                                       Auth,
                                       RemoteUser,
                                       Message,
                                       XFrame,
                                       UserService),
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND)
                   )
class TestDispatchErrorCases(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage(self):
        url = reverse("myuw_book_api",
                      kwargs={'year': 2013,
                              'quarter': 'spring',
                              'summer_term': ''})
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))

        response = self.client.put(url)
        self.assertEquals(response.status_code, 405)

        response = self.client.post(url)
        self.assertEquals(response.status_code, 405)

        response = self.client.delete(url)
        self.assertEquals(response.status_code, 405)
