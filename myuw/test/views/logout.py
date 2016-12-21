from unittest2 import skipIf
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from myuw.test.api import missing_url, MyuwApiTest
from myuw.test.views import get_desktop_args


LOGOUT_URL = "/user_logout"


class TestLogoutLink(MyuwApiTest):

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_logout(self):
        logout_url = reverse("myuw_logout")
        home_url = reverse("myuw_home")
        self.set_user('javerage')
        old_session_id = self.client.cookies['sessionid'].value
        response = self.client.get(logout_url, **get_desktop_args())
        new_session_id = self.client.cookies['sessionid'].value
        self.assertNotEqual(old_session_id, new_session_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], LOGOUT_URL)
