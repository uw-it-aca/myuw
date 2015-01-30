from django.test import TestCase
from django.conf import settings
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
from myuw_mobile.dao.term import get_current_term
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

class TestDisplayDatesPage(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_mobile.views.display_dates.override"), "display dates override urls not configured")
    def test_override(self):
        url = reverse("myuw_mobile.views.display_dates.override")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))

        response = self.client.post(url, {'date':'2013-06-07', 'myuw_after_submission':'no', 'myuw_after_reg':'yes'})
        self.assertEquals(response.status_code, 200)    
        self.assertEqual(self.client.session['myuw_override_date'], '2013-06-07')

        response = self.client.post(url, {'date':'2013-02-07', 'myuw_after_reg':'blah'})
        self.assertEquals(response.status_code, 200)    
        self.assertEqual(self.client.session['myuw_override_date'], '2013-02-07')

        response = self.client.post(url, {'date':'2012-11-07'})
        self.assertEquals(response.status_code, 200)    
        self.assertEqual(self.client.session['myuw_override_date'], '2012-11-07')

    @skipIf(missing_url("myuw_mobile.views.display_dates.override"), "display dates override urls not configured")
    @override_settings(USERSERVICE_ADMIN_GROUP='test group')
    def test_no_admin_group(self):
        del settings.USERSERVICE_ADMIN_GROUP
        url = reverse("myuw_mobile.views.display_dates.override")
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))

        with self.assertRaises(Exception):
            self.client.get(url)

        
