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
class TestOtherQuarters(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_oquarters(self):
        url = reverse("myuw_other_quarters_api")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data["next_term_data"]["has_registration"], True)
        self.assertEquals(data["next_term_data"]["quarter"], "Autumn")
        self.assertEquals(data["next_term_data"]["year"], 2013)

        self.assertEquals(len(data["terms"]), 3)

        self.assertEquals(data["terms"][0]['section_count'], 2)
        self.assertEquals(data["terms"][0]['url'], '/2013,summer,a-term')
        self.assertEquals(data["terms"][0]['summer_term'], 'a-term')
        self.assertEquals(data["terms"][0]['year'], 2013)
        self.assertEquals(data["terms"][0]['quarter'], 'Summer')
        self.assertEquals(data["terms"][0]['credits'], '2.0')
        self.assertEquals(data["terms"][0]['last_final_exam_date'], '2013-08-23 23:59:59')
