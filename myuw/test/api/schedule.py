from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw.test.api import missing_url, get_user, get_user_pass
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
class TestSchedule(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_javerage_current_term(self):
        url = reverse("myuw_current_schedule")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 5)
        for section in data["sections"]:
            if section["curriculum_abbr"] == "PHYS" and\
                    section["course_number"] == "121" and\
                    section["section_id"] == "A":
                self.assertEquals(section["canvas_url"],
                                  "https://canvas.uw.edu/courses/249652")
                self.assertEquals(section["canvas_name"],
                                  "MECHANICS")

            if section["curriculum_abbr"] == "TRAIN" and\
                    section["course_number"] == "100" and\
                    section["section_id"] == "A":
                self.assertRaises(KeyError, section.get("canvas_url"))

    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_none_current_term(self):
        url = reverse("myuw_current_schedule")
        get_user('none')
        self.client.login(username='none', password=get_user_pass('none'))
        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.content, 'Data not found')

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
        get_user('jerror')
        self.client.login(username='jerror',
                          password=get_user_pass('jerror'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 543)

    @skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
    def test_summer_terms(self):
        url = reverse("myuw_current_schedule")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
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
