import datetime
import pytz
import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings


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
class TestIasystemApi(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_iasystem_api"), "ias urls not configured")
    def test_javerage_normal_cases(self):
        url = reverse("myuw_iasystem_api")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

        # after show date 2013 Spring
        session = self.client.session
        session["myuw_override_date"] = "2013-05-31"
        session.save()
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 5)

        # before show date
        session = self.client.session
        session["myuw_override_date"] = "2013-07-16"
        session.save()

        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

        # after show date
        session = self.client.session
        session["myuw_override_date"] = "2013-07-17"
        session.save()

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Summer')
        self.assertEquals(len(data["sections"]), 2)
        eval = data["sections"][0]["evaluation_data"]
        self.assertEquals(len(eval), 0)
        eval = data["sections"][1]["evaluation_data"]
        self.assertEquals(len(eval), 0)

    @skipIf(missing_url("myuw_iasystem_api"), "ias urls not configured")
    def test_eight_2013_spring(self):
        url = reverse("myuw_iasystem_api")
        get_user('eight')
        self.client.login(username='eight', password=get_user_pass('eight'))
        session = self.client.session
        session["myuw_override_date"] = "2013-06-08"
        session.save()
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 8)

    @skipIf(missing_url("myuw_iasystem_api"), "ias urls not configured")
    def test_user_none(self):
        url = reverse("myuw_iasystem_api")
        get_user('none')
        self.client.login(username='none', password=get_user_pass('none'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    @skipIf(missing_url("myuw_iasystem_api"), "ias urls not configured")
    def test_missing_current_term(self):
        url = reverse("myuw_iasystem_api")
        get_user('err_user')
        self.client.login(username='err_user',
                          password=get_user_pass('err_user'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    @skipIf(missing_url("myuw_iasystem_api"), "ias urls not configured")
    def test_summer_terms(self):
        url = reverse("myuw_iasystem_api")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        session = self.client.session
        session["myuw_override_date"] = "2013-07-24"
        session.save()

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Summer')
        self.assertEquals(data["summer_term"], "a-term")
        self.assertEquals(len(data["sections"]), 2)

        eval = data["sections"][0]["evaluation_data"]
        self.assertEquals(len(eval), 1)
        self.assertEquals(eval[0]['close_date'],
                          "2013-07-29 06:59:59 UTC+0000")

        eval = data["sections"][1]["evaluation_data"]
        self.assertEquals(len(eval), 0)

        session = self.client.session
        session["myuw_override_date"] = "2013-08-27"
        session.save()

        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEquals(data["summer_term"], "b-term")
        self.assertEquals(len(data["sections"]), 2)

        eval = data["sections"][0]["evaluation_data"]
        self.assertEquals(len(eval), 0)

        eval = data["sections"][1]["evaluation_data"]
        self.assertEquals(len(eval), 1)
        self.assertEquals(eval[0]['close_date'],
                          "2013-08-29 06:59:59 UTC+0000")
