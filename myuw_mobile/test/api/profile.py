from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from myuw_mobile.dao.student_profile import __name__ as student_profile_dao_name
from logging.handlers import MemoryHandler
import logging
import json


@override_settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                   MIDDLEWARE_CLASSES=(
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
class TestProfile(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_books(self):
        url = reverse("myuw_profile_api")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["first_name"], "John Joseph")
        self.assertEquals(data["last_name"], "Average")
        self.assertEquals(data["local_address"]["street_line1"], "4634 26th Ave NE")
        self.assertEquals(data["local_address"]["zip_code"], "98105-4566")
        self.assertEquals(data["student_number"], "1033334")

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_missing_regid(self):
        logger = logging.getLogger(student_profile_dao_name)
        handler = MemoryHandler(100, flushLevel=60)
        logger.addHandler(handler)
        
        url = reverse("myuw_profile_api")
        get_user('err_user')
        self.client.login(username='err_user', password=get_user_pass('err_user'))
        self.client.get(url)

        for log in handler.buffer:
            self.assertIn('in get_profile_of_current_user', log.msg)
