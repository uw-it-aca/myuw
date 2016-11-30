from unittest2 import skipIf
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from myuw.models import UserMigrationPreference
from myuw.test.api import missing_url, require_url, MyuwApiTest


old_valid_url = "http://some.washington.edu/servlet/user"
override_servlet_url = override_settings(MYUW_USER_SERVLET_URL=old_valid_url)


@require_url('myuw_home')
@override_servlet_url
class TestChoose(MyuwApiTest):

    @skipIf(missing_url("myuw_pref_old_site"),
            "myuw_pref_old_site urls not configured")
    def test_choose_old(self):
        UserMigrationPreference.objects.all().delete()
        username = "test_set_pref"
        self.set_user(username)
        url = reverse("myuw_pref_old_site")
        response = self.get_response(url)
        obj = UserMigrationPreference.objects.get(username=username)
        self.assertTrue(obj.use_legacy_site)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), old_valid_url)

        response = self.get_response(url)
        obj = UserMigrationPreference.objects.get(username=username)
        self.assertTrue(obj.use_legacy_site)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), old_valid_url)

        url = reverse("myuw_pref_new_site")
        response = self.get_response(url)
        obj = UserMigrationPreference.objects.get(username=username)
        self.assertFalse(obj.use_legacy_site)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response["Location"], '/')
        UserMigrationPreference.objects.all().delete()

    @skipIf(missing_url("myuw_pref_new_site"),
            "myuw_pref_new_site urls not configured")
    def test_choose_new(self):
        UserMigrationPreference.objects.all().delete()
        username = "test_set_pref"
        self.set_user(username)
        url = reverse("myuw_pref_new_site")
        response = self.get_response(url)
        obj = UserMigrationPreference.objects.get(username=username)
        self.assertFalse(obj.use_legacy_site)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response["Location"], '/')

        response = self.get_response(url)
        obj = UserMigrationPreference.objects.get(username=username)
        self.assertFalse(obj.use_legacy_site)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response["Location"], '/')

        url = reverse("myuw_pref_old_site")
        response = self.get_response(url)
        obj = UserMigrationPreference.objects.get(username=username)
        self.assertTrue(obj.use_legacy_site)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), old_valid_url)
        UserMigrationPreference.objects.all().delete()

    def get_response(self, url):
        return self.client.get(url)
