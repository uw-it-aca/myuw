from unittest2 import skipIf
from django.test.utils import override_settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from myuw.test.api import missing_url, get_user, get_user_pass


Session = 'django.contrib.sessions.middleware.SessionMiddleware'
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
RemoteUser = 'django.contrib.auth.middleware.RemoteUserMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'

LOGOUT_URL = "%s%s" % ('https://weblogin.washington.edu/',
                       '?logout_action=1&two=myuw&one=myuw.washington.edu')


@override_settings(MIDDLEWARE_CLASSES=(Session,
                                       Common,
                                       CsrfView,
                                       Auth,
                                       RemoteUser,
                                       Message,
                                       XFrame,
                                       UserService,
                                       ),
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND,)
                   )
class TestLogoutLink(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_logout(self):
        logout_url = reverse("myuw_logout")
        home_url = reverse("myuw_home")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        old_session_id = self.client.cookies['sessionid'].value
        response = self.client.get(logout_url, **_get_desktop_args())
        new_session_id = self.client.cookies['sessionid'].value
        self.assertNotEqual(old_session_id, new_session_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], LOGOUT_URL)


def _get_desktop_args():
    return {'HTTP_USER_AGENT': ("Mozilla/5.0 (compatible; MSIE 10.0; Windows "
                                "NT 6.2; ARM; Trident/6.0; Touch)")}
