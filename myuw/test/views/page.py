from unittest2 import skipIf
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from myuw.views.page import _is_mobile
from myuw.test.api import missing_url, MyuwApiTest


legacy_url="http://some-test-server/myuw"


@override_settings(MYUW_USER_SERVLET_URL=legacy_url)
class TestPageMethods(MyuwApiTest):

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
        self.set_user('jnone')
        response = self.client.get(url,
                                   HTTP_USER_AGENT='Fake Android Mobile')
        self.assertEquals(response.status_code, 302)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_desktop_redirect(self):
        url = reverse("myuw_home")
        self.set_user('testcal1')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEquals(response.status_code, 302)

        self.set_user('staff')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEquals(response.status_code, 302)

        self.set_user('faculty')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEquals(response.status_code, 302)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_undergrad_access(self):
        url = reverse("myuw_home")
        self.set_user('jbothell')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_support_links(self):
        url = reverse("myuw_date_override")
        self.set_user('jbothell')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_non_student_mobile(self):
        url = reverse("myuw_home")
        self.set_user('faculty')
        response = self.client.get(
            url,
            HTTP_USER_AGENT='Fake iPhone Agent')
        self.assertEquals(response.status_code, 302)
