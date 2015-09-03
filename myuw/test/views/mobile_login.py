from django.test import TestCase
from django.conf import settings
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw.test.api import missing_url, get_user, get_user_pass
from myuw.models import UserMigrationPreference
from django.test.utils import override_settings
import json


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
class TestLoginRedirects(TestCase):
    def setUp(self):
        self.client = Client()

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_student_mobile(self):
        url = reverse("myuw_home")
        get_user('javerage')
        self.client.login(username='javerage',
                          password=get_user_pass('javerage'))
        response = self.client.get(url, **_get_mobile_args())

        valid_url = "http://testserver%s" % reverse("myuw_home")
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    # Putting this here to remove it, to make sure we're testing the default
    @override_settings(MYUW_USER_SERVLET_URL="http://some-test-server/myuw")
    def test_random_non_student_mobile(self):
        del settings.MYUW_USER_SERVLET_URL
        url = reverse("myuw_home")
        get_user('random')
        self.client.login(username='random', password=get_user_pass('random'))
        response = self.client.get(url, **_get_mobile_args())

        # This is the default...
        valid_url = "https://myuw.washington.edu/servlet/user"
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), valid_url)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    @override_settings(MYUW_USER_SERVLET_URL="http://some-test-server/myuw")
    def test_random_non_student_mobile_override_url(self):
        url = reverse("myuw_home")
        get_user('random')
        self.client.login(username='random', password=get_user_pass('random'))
        response = self.client.get(url, **_get_mobile_args())

        valid_url = "http://some-test-server/myuw"
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), valid_url)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    @override_settings(MYUW_USER_SERVLET_URL="http://some-test-server/myuw")
    def test_random_desktop_user(self):
        url = reverse("myuw_home")
        get_user('random2')
        self.client.login(username='random2', password=get_user_pass('random'))
        response = self.client.get(url, **_get_desktop_args())

        valid_url = "http://some-test-server/myuw"
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), valid_url)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    @override_settings(MYUW_USER_SERVLET_URL="http://some-test-server/myuw")
    # Putting this here to remove it, to make sure we're testing the default
    @override_settings(MYUW_MANDATORY_SWITCH_PATH="/tmp/xx")
    def test_required_migration_desktop_user(self):
        del settings.MYUW_MANDATORY_SWITCH_PATH
        url = reverse("myuw_home")
        get_user('47e5e5631c3d3e0ad70047290a629c4c')
        self.client.login(username='47e5e5631c3d3e0ad70047290a629c4c',
                          password=get_user_pass('random'))
        response = self.client.get(url, **_get_desktop_args())

        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    @override_settings(MYUW_USER_SERVLET_URL="http://some-test-server/myuw")
    # Putting this here to remove it, to make sure we're testing the default
    @override_settings(MYUW_OPTIN_SWITCH_PATH="/tmp/xx")
    def test_required_migration_desktop_user(self):
        del settings.MYUW_OPTIN_SWITCH_PATH

        # Delete any preference that might have been set, to test the
        # default state.
        UserMigrationPreference.objects.all().delete()
        username = "cfcd208495d565ef66e7dff9f98764da"
        url = reverse("myuw_home")
        get_user(username)
        self.client.login(username=username,
                          password=get_user_pass('random'))
        response = self.client.get(url, **_get_desktop_args())

        # By default, they get sent to the new site
        self.assertEquals(response.status_code, 200)

        # Test with a saved preference of the old site
        obj = UserMigrationPreference.objects.create(username=username,
                                                     use_legacy_site=True)

        response = self.client.get(url, **_get_desktop_args())

        valid_url = "http://some-test-server/myuw"
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), valid_url)

        # Test with a saved preference for the new site
        obj.use_legacy_site = False
        obj.save()
        response = self.client.get(url, **_get_desktop_args())
        self.assertEquals(response.status_code, 200)

    @override_settings(MYUW_USER_SERVLET_URL="http://some-test-server/myuw")
    def test_set_legacy_preferences(self):
        # Clear any existing data...
        UserMigrationPreference.objects.all().delete()

        username = "test_set_pref"
        new_url = reverse('myuw_pref_new_site')
        old_url = reverse('myuw_pref_old_site')

        # Set a preference for the new site, with no existing preference
        get_user(username)
        self.client.login(username=username,
                          password=get_user_pass(username))
        response = self.client.get(new_url)

        new_valid_url = "http://testserver/mobile/"
        old_valid_url = "http://some-test-server/myuw"
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), new_valid_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertFalse(obj.use_legacy_site)

        # Set a preference again for the new site
        response = self.client.get(new_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), new_valid_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertFalse(obj.use_legacy_site)

        # Go to the set old preference url, but don't post
        response = self.client.get(old_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), old_valid_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertFalse(obj.use_legacy_site)

        # POST to the set old preference url, changing preference
        response = self.client.post(old_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), old_valid_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertTrue(obj.use_legacy_site)

        # POST again
        response = self.client.post(old_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), old_valid_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertTrue(obj.use_legacy_site)

        # POST to the set old preference url, without an existing preference
        UserMigrationPreference.objects.all().delete()
        response = self.client.get(old_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), old_valid_url)

        with self.assertRaises(UserMigrationPreference.DoesNotExist):
            UserMigrationPreference.objects.get(username=username)

        # Replace a legacy preference with a new one
        response = self.client.get(new_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), new_valid_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertFalse(obj.use_legacy_site)


def _get_mobile_args():
    return {'HTTP_USER_AGENT': ("Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 "
                                "like Mac OS X) AppleWebKit/536.26 (KHTML, "
                                "like Gecko) Version/6.0 Mobile/10B329 "
                                "Safari/8536.25")}


def _get_desktop_args():
    return {'HTTP_USER_AGENT': ("Mozilla/5.0 (compatible; MSIE 10.0; Windows "
                                "NT 6.2; ARM; Trident/6.0; Touch)")}
