from django.conf import settings
from django.core.urlresolvers import reverse
from myuw.test.api import MyuwApiTest, require_url
from myuw.models import UserMigrationPreference
from django.test.utils import override_settings


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
        self.set_user('staff')
        response = self.get_home_mobile()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), redirect_to_legacy_url)

    def test_non_student_non_optin_mobile(self):
        self.set_user('curgrad')
        response = self.get_home_mobile()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), redirect_to_legacy_url)

    def test_random_desktop_user(self):
        url = reverse("myuw_home")
        self.set_user('staff1')
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), redirect_to_legacy_url)

        self.set_user('jnew')
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)

        UserMigrationPreference.objects.all().delete()
        username = "jbothell"
        self.set_user(username)
        response = self.get_home_desktop()

        # By default, they get sent to the new site
        self.assertEquals(response.status_code, 200)

        # Test with a saved preference of the old site
        regid = "jbothell"
        obj = UserMigrationPreference.objects.create(username=regid,
                                                     use_legacy_site=True)

        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), redirect_to_legacy_url)

        # Test with a saved preference for the new site
        obj.use_legacy_site = False
        obj.save()
        response = self.get_home_desktop()
        self.assertEquals(response.status_code, 200)
        UserMigrationPreference.objects.all().delete()

    def test_set_legacy_preferences(self):
        # Clear any existing data...
        UserMigrationPreference.objects.all().delete()

        username = "test_set_pref"
        new_url = reverse('myuw_pref_new_site')
        old_url = reverse('myuw_pref_old_site')

        # Set a preference for the new site, with no existing preference
        self.set_user(username)
        response = self.client.get(new_url)

        new_valid_url = "/"
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

        # Go to the set old preference url
        response = self.client.get(old_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), redirect_to_legacy_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertTrue(obj.use_legacy_site)

        response = self.client.post(old_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), redirect_to_legacy_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertTrue(obj.use_legacy_site)

        # Replace a legacy preference with a new one
        response = self.client.get(new_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get("Location"), new_valid_url)

        obj = UserMigrationPreference.objects.get(username=username)
        self.assertFalse(obj.use_legacy_site)
