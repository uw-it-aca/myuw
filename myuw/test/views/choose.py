from unittest2 import skipIf
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from myuw.dao.user_pref import has_legacy_preference
from myuw.test import get_request_with_user
from myuw.test.api import missing_url, require_url, MyuwApiTest


old_valid_url = "http://some.washington.edu/servlet/user"
override_servlet_url = override_settings(MYUW_USER_SERVLET_URL=old_valid_url)


@require_url('myuw_home')
@override_servlet_url
class TestChoose(MyuwApiTest):

    @skipIf(missing_url("myuw_pref_old_site"),
            "myuw_pref_old_site urls not configured")
    def test_choose_old(self):
        username = "jnew"
        self.set_user(username)
        url = reverse("myuw_pref_old_site")
        response = self.get_response(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), old_valid_url)
        self.assertTrue(
            has_legacy_preference(get_request_with_user(username)))

        url = reverse("myuw_pref_new_site")
        response = self.get_response(url)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response["Location"], '/')
        self.assertFalse(
            has_legacy_preference(get_request_with_user(username)))

    def get_response(self, url):
        return self.client.get(url)
