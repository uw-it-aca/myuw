from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from unittest2 import skipIf
import json
from myuw_mobile.test.api import missing_url, get_user, get_user_pass

@override_settings(RESTCLIENTS_HFS_DAO_CLASS='myuw_mobile.restclients.dao_implementation.hfs.File',
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
class TestHFS(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage(self):
        url = reverse("myuw_hfs_api")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))

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
        self.client.login(username='err-user', password=get_user_pass('javerage'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertFalse("employee_husky_card" in data)
        self.assertFalse("resident_dining" in data)
        self.assertFalse("student_husky_card" in data)

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
