import json
from unittest2 import skipIf
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from myuw_mobile.test.api import missing_url, get_user, get_user_pass


FDAO_SWS = 'restclients.dao_implementation.sws.File'
SESSION = 'django.contrib.sessions.middleware.SessionMiddleware'
COMMON = 'django.middleware.common.CommonMiddleware'
CSRF_VIEW = 'django.middleware.csrf.CsrfViewMiddleware'
AUTH = 'django.contrib.auth.middleware.AuthenticationMiddleware'
REMOTE_USER = 'django.contrib.auth.middleware.RemoteUserMiddleware'
MESSAGE = 'django.contrib.messages.middleware.MessageMiddleware'
XFRAME = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
USER_SERVICE = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'


@override_settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                   MIDDLEWARE_CLASSES=(SESSION,
                                       COMMON,
                                       CSRF_VIEW,
                                       AUTH,
                                       REMOTE_USER,
                                       MESSAGE,
                                       XFRAME,
                                       USER_SERVICE,
                                       ),
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND,)
                   )
class TestUWEmail(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_email(self):
        url = reverse("myuw_email_api")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data["status"], "Active")
        self.assertEquals(data["fwd"], "javerage@gamail.uw.edu")
        self.assertEquals(data["is_active"], True)
        self.assertEquals(data["is_uwlive"], False)
        self.assertEquals(data["is_uwgmail"], True)
        self.assertEquals(data["permitted"], True)
