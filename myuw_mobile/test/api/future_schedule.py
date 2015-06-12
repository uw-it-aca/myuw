from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
import json


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
                                       UserService,),
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND,)
                   )
class TestFutureSchedule(TestCase):

    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_future(self):
        url = reverse("myuw_future_schedule_api",
                      kwargs={'year': 2013,
                              'quarter': 'autumn'})
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data["sections"]), 1)

        url = reverse("myuw_future_schedule_api",
                      kwargs={'year': 2015,
                              'quarter': 'autumn'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

        url = reverse("myuw_future_summer_schedule_api",
                      kwargs={'year': 2013,
                              'quarter': 'summer',
                              'summer_term': 'a-term'})
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data["sections"]), 2)

        url = reverse("myuw_future_summer_schedule_api",
                      kwargs={'year': 2013,
                              'quarter': 'summer',
                              'summer_term': 'b-term'})
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data["sections"]), 2)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_past_quarter(self):
        url = reverse("myuw_future_schedule_api",
                      kwargs={'year': 2013,
                              'quarter': 'winter'})
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 410)

        session = self.client.session
        session["myuw_override_date"] = "2013-03-26"
        session.save()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 410)

        session = self.client.session
        session["myuw_override_date"] = "2013-03-27"
        session.save()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        session = self.client.session
        session["myuw_override_date"] = "2013-04-01"
        session.save()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 410)
