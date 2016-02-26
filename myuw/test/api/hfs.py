from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from unittest2 import skipIf
import json
from myuw.test.api import missing_url, get_user, get_user_pass


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
class TestHFS(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage(self):
        url = reverse("myuw_hfs_api")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data["employee_husky_card"]["balance"], 1)
        self.assertEquals(data["resident_dining"]["balance"], 5.1)
        self.assertEquals(data["student_husky_card"]["balance"], 1.23)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_bad_user(self):
        url = reverse("myuw_hfs_api")
        get_user('err-user')
        self.client.login(username='err-user',
                          password=get_user_pass('javerage'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

        get_user('none')
        self.client.login(username='none',
                          password=get_user_pass('javerage'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_error(self):
        url = reverse("myuw_hfs_api")
        get_user('jerror')
        self.client.login(username='jerror',
                          password=get_user_pass('javerage'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 543)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_eight(self):
        url = reverse("myuw_hfs_api")
        get_user('eight')
        self.client.login(username='eight', password=get_user_pass('eight'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data["employee_husky_card"], None)
        self.assertEquals(data["resident_dining"]["balance"], 15.1)
        self.assertEquals(data["student_husky_card"]["balance"], 100.23)
