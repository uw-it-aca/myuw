from unittest import skipIf
from unittest.mock import patch
from django.urls import reverse
from django.test.client import RequestFactory
from myuw.test.api import missing_url, MyuwApiTest


class TestPageMethods(MyuwApiTest):

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_not_in_pws_applicant_access(self):
        url = reverse("myuw_home")
        self.set_user('jnone')
        response = self.client.get(url,
                                   HTTP_USER_AGENT='Fake Android Mobile')
        self.assertEquals(response.status_code, 400)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_desktop_redirect(self):
        url = reverse("myuw_home")
        self.set_user('nobody')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEquals(response.status_code, 200)

        self.set_user('faculty')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_undergrad_access(self):
        url = reverse("myuw_home")
        self.set_user('jbothell')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_access(self):
        with self.settings(
                MYUW_PROD_URL="https://my.uw",
                MYUW_TEST_ACCESS_GROUP='u_astratst_myuw_test-support-admin'):
            url = reverse("myuw_home")
            self.set_user('jbothell')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 403)

            self.set_user('bill')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_support_links(self):
        url = reverse("myuw_date_override")
        self.set_user('jbothell')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_non_student_mobile(self):
        url = reverse("myuw_home")
        self.set_user('faculty')
        response = self.client.get(
            url,
            HTTP_USER_AGENT='Fake iPhone Agent')
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_instructor_access(self):
        url = reverse("myuw_home")
        self.set_user('bill')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_instructor(self):
        with self.settings(MYUW_ENABLED_FEATURES=['a']):
            url = reverse("myuw_home")
            self.set_user('bill')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.context["banner_messages"], [])
            self.assertEquals(response.context["display_onboard_message"],
                              True)
            self.assertEquals(response.context["display_pop_up"], True)
            self.assertEquals(response.context["disable_actions"], False)
            self.assertIsNotNone(response.context["card_display_dates"])
            self.assertIsNotNone(response.context["user"]["affiliations"])
            self.assertEquals(response.context["user"]['email_forward_url'],
                              'http://alpine.washington.edu')
            self.assertIsNone(response.context['google_search_key'])
            self.assertIsNotNone(response.context['enabled_features'])

            self.set_user('billpce')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

            self.set_user('billseata')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_no_user_in_session(self):
        # MUWM-4366
        url = reverse("myuw_home")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/saml/login?next=/")

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_user_not_in_pws(self):
        url = reverse("myuw_home")
        self.set_user('usernotinpws')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 400)

    @patch('myuw.views.page.get_updated_user', spec=True)
    def test_pws_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = Exception("mock")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 500)

    @patch('myuw.views.page.get_card_visibilty_date_values', spec=True)
    def test_sws_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = Exception("mock")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    @patch('myuw.views.page.get_email_forwarding_for_current_user', spec=True)
    def test_email_forward__err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = Exception("mock")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

