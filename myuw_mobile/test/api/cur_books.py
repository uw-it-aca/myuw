from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw_mobile.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
import json


FDAO_SWS = 'restclients.dao_implementation.sws.File'
Session = 'django.contrib.sessions.middleware.SessionMiddleware',
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
RemoteUser = 'django.contrib.auth.middleware.RemoteUserMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'
VERBACOMPARE_URL_PREFIX = 'http://uw-seattle.verbacompare.com'
IMAGE_URL_PREFIX = 'www7.bookstore.washington.edu/MyUWImage.taf'


@override_settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                   MIDDLEWARE_CLASSES=(SessionMiddleware
                                       Common,
                                       CsrfView,
                                       Auth,
                                       RemoteUser,
                                       Message,
                                       XFrame,
                                       UserService),
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND)
                   )
class TestCurBooks(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_current_book"),
            "myuw_current_book url not configured")
    def test_javerage_cur_term_books(self):
        url = reverse("myuw_current_book")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data["18545"]), 2)
        self.assertEquals(
            data["verba_link"],
            "%s/m?section_id=AB12345&quarter=spring" % VERBACOMPARE_URL_PREFIX)
        self.assertEquals(
            data["18545"][0]["cover_image_url"],
            ("%s?isbn=9780878935970&key=46c9ef715edb2ec69517e2c8e6ec9c18" %
             IMAGE_URL_PREFIX))
        self.assertEquals(len(data["18545"][0]["authors"]), 1)
        self.assertEquals(data["18545"][0]["is_required"], True)
        self.assertEquals(data["18545"][0]["price"], None)
        self.assertEquals(data["18545"][0]["used_price"], None)
        self.assertEquals(data["18545"][0]["isbn"], '9780878935970')
        self.assertEquals(data["18545"][0]["notes"], 'required')

    @skipIf(missing_url("myuw_current_book"),
            "myuw_current_book url not configured")
    def test_eight_cur_term_books(self):
        url = reverse("myuw_current_book")
        get_user('eight')
        self.client.login(username='eight', password=get_user_pass('eight'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data["11646"]), 1)
        self.assertEquals(data["11646"][0]["cover_image_url"], None)
        self.assertEquals(len(data["11646"][0]["authors"]), 1)
        self.assertEquals(data["11646"][0]["is_required"], True)
        self.assertEquals(data["11646"][0]["price"], 45.0)
        self.assertEquals(data["11646"][0]["used_price"], None)
        self.assertEquals(data["11646"][0]["isbn"], "9780521600491")
        self.assertEquals(data["11646"][0]["notes"], 'required')
