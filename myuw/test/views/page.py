import json
from unittest2 import skipIf
from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from myuw.views.page import _is_mobile
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
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND,),
                   MYUW_USER_SERVLET_URL="http://some-test-server/myuw",
                   )
class TestPageMethods(TestCase):
    def setUp(self):
        self.client = Client()

    def test_mobile_check(self):
        request = RequestFactory().get("/",
                                       HTTP_USER_AGENT='Fake iPhone Agent')
        self.assertTrue(_is_mobile(request))

        request = RequestFactory().get("/",
                                       HTTP_USER_AGENT='Fake Android Mobile')
        self.assertTrue(_is_mobile(request))

        request = RequestFactory().get("/",
                                       HTTP_USER_AGENT='Fake Android Agent')
        self.assertFalse(_is_mobile(request))

        request = RequestFactory().get("/", HTTP_USER_AGENT=None)
        self.assertFalse(_is_mobile(request))

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_not_in_pws_applicant_access(self):
        url = reverse("myuw_home")
        get_user('jnone')
        self.client.login(username='jnone',
                          password=get_user_pass('jnone'))
        response = self.client.get(url,
                                   HTTP_USER_AGENT='Fake Android Mobile')
        self.assertEquals(response.status_code, 302)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_desktop_redirect(self):
        url = reverse("myuw_home")
        get_user('testcal1')
        self.client.login(username='testcal1',
                          password=get_user_pass('testcal1'))
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEquals(response.status_code, 302)

        get_user('staff')
        self.client.login(username='staff',
                          password=get_user_pass('staff'))
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEquals(response.status_code, 302)

        get_user('faculty')
        self.client.login(username='faculty',
                          password=get_user_pass('faculty'))
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEquals(response.status_code, 302)


    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_undergrad_access(self):
        url = reverse("myuw_home")
        get_user('jbothell')
        self.client.login(username='jbothell',
                          password=get_user_pass('jbothell'))
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEquals(response.status_code, 200)
