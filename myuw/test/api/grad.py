import json
from unittest2 import skipIf
from datetime import datetime
from django.test.utils import override_settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
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
class TestApiGrad(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage(self):
        url = reverse("myuw_grad_api")
        get_user('seagrad')
        self.client.login(username='seagrad',
                          password=get_user_pass('seagrad'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.content)
        data = json.loads(response.content)

        self.assertIsNotNone(data.get("degrees"))
        self.assertEquals(len(data["degrees"]), 8)
        degree = data["degrees"][0]
        self.assertEqual(degree["req_type"], "Masters Request")
        self.assertEqual(degree["submit_date"], "2013-03-11T20:53:32")
        self.assertEqual(
            degree["degree_title"],
            "Master Of Landscape Architecture/Master Of Architecture")
        self.assertEqual(degree["major_full_name"],
                         "Landscape Arch/Architecture (Concurrent)")
        self.assertEqual(degree["status"],
                         "Awaiting Dept Action")
        self.assertIsNone(degree["exam_place"])
        self.assertIsNone(degree["exam_date"])
        self.assertEqual(degree["target_award_year"], 2013)
        self.assertEqual(degree["target_award_quarter"], "Spring")
        # committees
        self.assertIsNotNone(data.get("committees"))
        self.assertEquals(len(data["committees"]), 3)
        committee = data["committees"][0]
        self.assertEqual(committee['committee_type'], "Advisor")
        self.assertEqual(committee['status'], "active")
        self.assertEqual(committee['dept'], "Anthropology")
        self.assertEqual(committee['degree_title'], None)
        self.assertEqual(committee['degree_type'],
                         "Master Of Public Health (Epidemiology)")
        self.assertEqual(committee['major_full_name'], "ANTH")
        self.assertEqual(committee['start_date'],
                         "2012-12-07T08:26:14")
        self.assertEqual(len(committee['members']), 1)
        # leaves
        self.assertIsNotNone(data.get("leaves"))
        self.assertEquals(len(data["leaves"]), 3)
        leave = data["leaves"][0]
        self.assertEqual(leave['reason'],
                         "Dissertation/Thesis research/writing")
        self.assertEqual(leave['submit_date'],
                         "2012-09-10T09:40:03")
        self.assertEqual(leave['status'], "Requested")
        self.assertEqual(len(leave['terms']), 1)
        self.assertEqual(leave['terms'][0]['quarter'], "Spring")
        self.assertEqual(leave['terms'][0]['year'], 2013)
        # petitions
        self.assertIsNotNone(data.get("petitions"))
        self.assertEquals(len(data["petitions"]), 7)
        petition = data["petitions"][6]
        self.assertEqual(petition['description'],
                         "Doctoral degree - Extend ten year limit")
        self.assertEqual(petition['submit_date'],
                         "2013-04-06T16:32:28")
        self.assertEqual(petition['decision_date'],
                         "2013-04-10T00:00:00")
        self.assertEqual(petition['dept_recommend'], "Approve")
        self.assertEqual(petition['gradschool_decision'], "Approved")

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_error(self):
        url = reverse("myuw_grad_api")
        get_user('none')
        self.client.login(username='none',
                          password=get_user_pass('none'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.content, 'Data not found')

        get_user('jerror')
        self.client.login(username='jerror',
                          password=get_user_pass('jerror'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 543)
