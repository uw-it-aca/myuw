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
class TestBooks(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage_books(self):
        url = reverse("myuw_book_api", kwargs={'year': 2013, 'quarter': 'spring', 'summer_term': ''})
        get_user('javerage')
        self.client.login(username='javerage', password=get_user_pass('javerage'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["verba_link"], "http://uw-seattle.verbacompare.com/m?section_id=AB12345&quarter=spring")
        self.assertEquals(data["18545"][0]["cover_image_url"], "www7.bookstore.washington.edu/MyUWImage.taf?isbn=9780878935970&key=46c9ef715edb2ec69517e2c8e6ec9c18")
        self.assertEquals(len(data["18545"][0]["authors"]), 1)
        self.assertEquals(data["18545"][0]["is_required"], True)
        self.assertEquals(data["18545"][0]["price"], None)
        self.assertEquals(data["18545"][0]["used_price"], None)
        self.assertEquals(data["18545"][0]["isbn"], '9780878935970')
        self.assertEquals(data["18545"][0]["notes"], 'required')

        self.assertEquals(data["18545"][1]["price"], 44.0)
