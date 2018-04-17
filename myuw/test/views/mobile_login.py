from django.conf import settings
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from myuw.dao.user_pref import set_preference_to_old_myuw
from myuw.test import get_request_with_user
from myuw.test.api import MyuwApiTest, require_url


redirect_to_legacy_url = "https://myuw.washington.edu/servlet/user"
old_valid_url = "http://some-test-server/myuw"
override_servlet_url = override_settings(MYUW_USER_SERVLET_URL=old_valid_url)


@require_url('myuw_home')
@override_servlet_url
class TestLoginRedirects(MyuwApiTest):

    _mobile_args = {
        'HTTP_USER_AGENT': ("Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 "
                            "like Mac OS X) AppleWebKit/536.26 (KHTML, "
                            "like Gecko) Version/6.0 Mobile/10B329 "
                            "Safari/8536.25")}

    _desktop_args = {
        'HTTP_USER_AGENT': ("Mozilla/5.0 (compatible; MSIE 10.0; Windows "
                            "NT 6.2; ARM; Trident/6.0; Touch)")}

    def get_home_desktop(self):
        return self.client.get(reverse('myuw_home'), **self._desktop_args)

    def get_home_mobile(self):
        return self.client.get(reverse('myuw_home'), **self._mobile_args)

    def test_student_mobile(self):
        self.set_user('jnew')
        response = self.get_home_mobile()

        valid_url = reverse("myuw_home")
        self.assertEquals(response.status_code, 200)

    def test_non_student_mobile(self):
        del settings.MYUW_USER_SERVLET_URL
        self.set_user('japplicant')
        response = self.get_home_mobile()
        self.assertEquals(response.status_code, 200)

    def test_non_student_non_optin_mobile(self):
        self.set_user('curgrad')
        response = self.get_home_mobile()
        self.assertEquals(response.status_code, 200)

    def test_random_desktop_user(self):
        url = reverse("myuw_home")
        self.set_user('nobody')
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)

        self.set_user('jnew')
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)

        regid = "jbothell"
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)

    def test_set_legacy_preferences(self):
        username = "faculty"
        self.set_user(username)
        req = get_request_with_user(username)
        set_preference_to_old_myuw(req)

        self.set_user(username)
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), redirect_to_legacy_url)
