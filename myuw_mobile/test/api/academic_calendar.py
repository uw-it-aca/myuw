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
                                       UserService,
                                       ),
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND,)
                   )
class TestCalendarAPI(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_all_events(self):
        url = reverse("myuw_academic_calendar")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 29)

        session = self.client.session
        session["myuw_override_date"] = "2013-04-18"
        session.save()

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 28)

    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_muwm_2489(self):
        url = reverse("myuw_academic_calendar_current")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))

        session = self.client.session
        session["myuw_override_date"] = "2013-05-30"
        session.save()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 3)
        for event in data:
            self.assertNotEqual(event["summary"], "Memorial Day (no classes)")

    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_current_events(self):
        url = reverse("myuw_academic_calendar_current")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 4)

        session = self.client.session
        session["myuw_override_date"] = "2013-04-18"
        session.save()

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 3)

    # Test a workaround for MUWM-2522
    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_failing_term_resource(self):
        url = reverse("myuw_academic_calendar")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))

        session = self.client.session
        session["myuw_override_date"] = "2013-07-25"
        session.save()

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertTrue(len(data) > 1)
