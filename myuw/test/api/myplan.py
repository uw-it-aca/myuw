import json
from unittest2 import skipIf
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from myuw.test.api import missing_url, get_user, get_user_pass


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
class TestMyPlanApi(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_email(self):
        url = reverse("myuw_myplan_api",
                      kwargs={'year': 2013,
                              'quarter': 'autumn'})
        get_user('jinter')
        self.client.login(username='jinter',
                          password=get_user_pass('jinter'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data["terms"][0]["courses"]), 5)
        self.assertEquals(data["terms"][0]["has_unready_courses"], True)
        self.assertEquals(data["terms"][0]["has_ready_courses"], False)
        self.assertEquals(data["terms"][0]["has_sections"], True)
        self.assertEquals(data["terms"][0]["ready_count"], 0)
        self.assertEquals(data["terms"][0]["unready_count"], 5)

        url = reverse("myuw_myplan_api",
                      kwargs={'year': 2013,
                              'quarter': 'spring'})
        get_user('jinter')
        self.client.login(username='jinter',
                          password=get_user_pass('jinter'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(len(data["terms"][0]["courses"]), 6)
        self.assertEquals(data["terms"][0]["has_unready_courses"], False)
        self.assertEquals(data["terms"][0]["has_ready_courses"], True)
        self.assertEquals(data["terms"][0]["has_sections"], True)
        self.assertEquals(data["terms"][0]["ready_count"], 6)
        self.assertEquals(data["terms"][0]["unready_count"], 0)

    def test_error(self):
        url = reverse("myuw_myplan_api",
                      kwargs={'year': 2013,
                              'quarter': 'spring'})
        get_user('jerror')
        self.client.login(username='jerror',
                          password=get_user_pass('jerror'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')
