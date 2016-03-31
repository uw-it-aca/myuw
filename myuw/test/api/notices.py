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
class TestNotices(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_books(self):
        url = reverse("myuw_notices_api")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 23)

        self.assertEquals(data[0]["is_read"], False)

        hash_value = data[0]["id_hash"]

        response = self.client.put(
            url,
            data='{"notice_hashes":["%s"]}' % hash_value)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '')

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 23)

        match = False
        for el in data:
            if el["id_hash"] == hash_value:
                match = True
                self.assertEquals(el["is_read"], True)

        self.assertEquals(match, True)

        response = self.client.put(
            url, data='{"notice_hashes":["fake-fake-fake"]}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '')

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_error_cases(self):
        url = reverse("myuw_notices_api")
        get_user('jerror')
        self.client.login(username='jerror',
                          password=get_user_pass('jerror'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 543)

        get_user('staff')
        self.client.login(username='staff',
                          password=get_user_pass('staff'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_books(self):
        url = reverse("myuw_notices_api")
        get_user('jinter')
        self.client.login(username='jinter',
                          password=get_user_pass('jinter'))
        session = self.client.session
        session["myuw_override_date"] = "2013-04-26 00:00:00"
        session.save()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 31)
        for el in data:
            if el["category"] == "Registration" and\
                    'est_reg_date' in el["location_tags"]:
                self.assertFalse(el["is_my_1st_reg_day"])
                self.assertFalse(el["my_reg_has_opened"])

        session = self.client.session
        session["myuw_override_date"] = "2013-05-10 06:00:01"
        session.save()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 31)
        for el in data:
            if el["category"] == "Registration" and\
                    'est_reg_date' in el["location_tags"]:
                self.assertTrue(el["is_my_1st_reg_day"])
                self.assertTrue(el["my_reg_has_opened"])
