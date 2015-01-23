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

        self.assertEquals(data["18545"][0]["isbn"], "9780878935970")
        self.assertEquals(data["18545"][0]["title"], "Principles Of Conservation Biology (3e 06)")
        self.assertEquals(data["18545"][0]["price"], None)
        self.assertEquals(data["18545"][0]["is_required"], True)
        self.assertEquals(data["18545"][0]["used_price"], None)
        self.assertEquals(data["18545"][0]["authors"][0]["name"], "Groom")
        self.assertEquals(data["18545"][0]["cover_image_url"], "www7.bookstore.washington.edu/MyUWImage.taf?isbn=9780878935970&key=46c9ef715edb2ec69517e2c8e6ec9c18")
        self.assertEquals(data["18545"][0]["notes"], "required")
        self.assertEquals(data["18545"][1]["isbn"], "9781934931400")
        self.assertEquals(data["18545"][1]["title"], "Response Card Rf Lcd Radio Frequency ( Clicker )")
        self.assertEquals(data["18545"][1]["price"], 44.0)
        self.assertEquals(data["18545"][1]["is_required"], True)
        self.assertEquals(data["18545"][1]["used_price"], None)
        self.assertEquals(data["18545"][1]["authors"][0]["name"], "Turning Technologies")
        self.assertEquals(data["18545"][1]["cover_image_url"], "www7.bookstore.washington.edu/MyUWImage.taf?isbn=9781934931400&key=f66964a1341ff6e6518530eee30209a4")
        self.assertEquals(data["18545"][1]["notes"], "required")        
        
    def test_jbothell_books(self):
        url = reverse("myuw_book_api", kwargs={'year': 2013, 'quarter': 'spring', 'summer_term': ''})
        get_user('jbothell')
        self.client.login(username='jbothell', password=get_user_pass('jbothell'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        #self.assertEquals(data["verba_link"], "http://uw-seattle.verbacompare.com/m?section_id=AB12345&quarter=spring")
        self.assertEquals(data["11230"][0]["isbn"], "9781256396362")
        self.assertEquals(data["11230"][0]["title"], "Writ of BC")
        self.assertEquals(data["11230"][0]["price"], 58.0)
        self.assertEquals(data["11230"][0]["is_required"], True)
        self.assertEquals(data["11230"][0]["used_price"], None)
        self.assertEquals(data["11230"][0]["authors"][0]["name"], "Mcdermott")
        self.assertEquals(data["11230"][0]["cover_image_url"], None)
        self.assertEquals(data["11230"][0]["notes"], None)

        self.assertEquals(data["15612"][0]["isbn"], "9781256496062")
        self.assertEquals(data["15612"][0]["title"], "ESS Stuff 'n Things")
        self.assertEquals(data["15612"][0]["price"], 58.0)
        self.assertEquals(data["15612"][0]["is_required"], True)
        self.assertEquals(data["15612"][0]["used_price"], None)
        self.assertEquals(data["15612"][0]["authors"][0]["name"], "Mcdermott")
        self.assertEquals(data["15612"][0]["cover_image_url"], None)
        self.assertEquals(data["15612"][0]["notes"], None)

        self.assertEquals(data["14460"][0]["isbn"], "9785256396062")
        self.assertEquals(data["14460"][0]["title"], "Studies in Bissy Bee")
        self.assertEquals(data["14460"][0]["price"], 58.0)
        self.assertEquals(data["14460"][0]["is_required"], True)
        self.assertEquals(data["14460"][0]["used_price"], None)
        self.assertEquals(data["14460"][0]["authors"][0]["name"], "Mcdermott")
        self.assertEquals(data["14460"][0]["cover_image_url"], None)
        self.assertEquals(data["14460"][0]["notes"], None)

    def test_jnew_books(self):
        url = reverse("myuw_book_api", kwargs={'year': 2013, 'quarter': 'spring', 'summer_term': ''})
        get_user('jnew')
        self.client.login(username='jnew', password=get_user_pass('jnew'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["13833"][0]["isbn"], "9781256396362")
        self.assertEquals(data["13833"][0]["title"], "Writ of BC")
        self.assertEquals(data["13833"][0]["price"], 58.0)
        self.assertEquals(data["13833"][0]["is_required"], True)
        self.assertEquals(data["13833"][0]["used_price"], None)
        self.assertEquals(data["13833"][0]["authors"][0]["name"], "Mcdermott")
        self.assertEquals(data["13833"][0]["cover_image_url"], None)
        self.assertEquals(data["13833"][0]["notes"], None)

    def test_eight_books(self):
        url = reverse("myuw_book_api", kwargs={'year': 2013, 'quarter': 'spring', 'summer_term': ''})
        get_user('eight')
        self.client.login(username='eight', password=get_user_pass('eight'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["18532"][0]["isbn"], "9780878935970")
        self.assertEquals(data["18532"][0]["title"], "Principles Of Conservation Biology (3e 06)")
        self.assertEquals(data["18532"][0]["price"], None)
        self.assertEquals(data["18532"][0]["is_required"], True)
        self.assertEquals(data["18532"][0]["used_price"], None)
        self.assertEquals(data["18532"][0]["authors"][0]["name"], "Groom")
        self.assertEquals(data["18532"][0]["cover_image_url"], "www7.bookstore.washington.edu/MyUWImage.taf?isbn=9780878935970&key=46c9ef715edb2ec69517e2c8e6ec9c18")
        self.assertEquals(data["18532"][0]["notes"], "required")

        self.assertEquals(data["11646"][0]["isbn"], "9780521600491")
        self.assertEquals(data["11646"][0]["title"], "History Of Archaeological Thought (2e 06)")
        self.assertEquals(data["11646"][0]["price"], 45.0)
        self.assertEquals(data["11646"][0]["is_required"], True)
        self.assertEquals(data["11646"][0]["used_price"], None)
        self.assertEquals(data["11646"][0]["authors"][0]["name"], "Trigger")
        self.assertEquals(data["11646"][0]["cover_image_url"], None)
        self.assertEquals(data["11646"][0]["notes"], "required")


    
