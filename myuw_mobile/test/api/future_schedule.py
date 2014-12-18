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
class TestFutureSchedule(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_future(self):
        url = reverse("myuw_future_schedule_api", kwargs={'year': 2013, 'quarter':'autumn'})
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data["sections"]), 1)


        url = reverse("myuw_future_schedule_api", kwargs={'year': 2015, 'quarter':'autumn'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

        url = reverse("myuw_future_summer_schedule_api", kwargs={'year': 2013, 'quarter':'summer', 'summer_term': 'a-term'})
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data["sections"]), 2)

        url = reverse("myuw_future_summer_schedule_api", kwargs={'year': 2013, 'quarter':'summer', 'summer_term': 'b-term'})
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data["sections"]), 2)

        url = reverse("myuw_future_schedule_api", kwargs={'year': 2013, 'quarter':'winter'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 410)


