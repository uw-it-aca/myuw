from django.test import TestCase
from django.conf import settings
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings

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

class TestPageView(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_mobile.views.page.index"), "page index urls not configured")
    def test_override(self):
        url = reverse("myuw_mobile.views.page.index")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
