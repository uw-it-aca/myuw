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

class TestSchedule(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_javerage_current_term(self):
        url = reverse("myuw_current_schedule")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 5)


    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_none_current_term(self):
        url = reverse("myuw_current_schedule")
        get_user('none')
        self.client.login(username='none', password=get_user_pass('none'))
#        session = self.client.session
#        session["myuw_override_date"] = "2013-07-06"
#        session.save()
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 0)


    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_eight_current_term(self):
        url = reverse("myuw_current_schedule")
        get_user('eight')
        self.client.login(username='eight', password=get_user_pass('eight'))
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 8)


    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_missing_current_term(self):
        url = reverse("myuw_current_schedule")
        get_user('err_user')
        self.client.login(username='err_user', password=get_user_pass('err_user'))
        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)


    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_summer_terms(self):
        url = reverse("myuw_current_schedule")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        session = self.client.session
        session["myuw_override_date"] = "2013-07-06"
        session.save()

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Summer')
        self.assertEquals(data["summer_term"], "a-term")

        session = self.client.session
        session["myuw_override_date"] = "2013-07-25"
        session.save()

        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEquals(data["summer_term"], "b-term")
