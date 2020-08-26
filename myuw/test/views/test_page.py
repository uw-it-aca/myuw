from unittest import skipIf
from unittest.mock import patch
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils import timezone
from django.test.client import RequestFactory
from unittest.mock import patch
from myuw.models import User
from myuw.views.page import logout, page
from restclients_core.exceptions import DataFailureException
from myuw.dao.exceptions import EmailServiceUrlException
from myuw.dao.user import get_user_model
from myuw.test.api import missing_url, MyuwApiTest
from myuw.test import get_request_with_user


class TestPageMethods(MyuwApiTest):

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_not_in_pws_applicant_access(self):
        url = reverse("myuw_home")
        self.set_user('jnone')
        response = self.client.get(url,
                                   HTTP_USER_AGENT='Fake Android Mobile')
        self.assertEquals(response.status_code, 403)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_desktop_redirect(self):
        url = reverse("myuw_home")
        self.set_user('javerage')
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
                MYUW_SKIP_ACCESS_CHECK=False,
                MYUW_TEST_ACCESS_GROUP='u_astratst_myuw_test-support-admin'):
            url = reverse("myuw_home")
            self.set_user('jbothell')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 403)

            self.set_user('bill')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)
        with self.settings(
                MYUW_SKIP_ACCESS_CHECK=True,
                MYUW_TEST_ACCESS_GROUP='u_astratst_myuw_test-support-admin'):
            # MUWM-4710
            url = reverse("myuw_home")
            self.set_user('jbothell')
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

    @skipIf(missing_url("myuw_logout"), "myuw_logout not configured")
    def test_logout(self):
        self.set_user('javerage')
        url = reverse("myuw_logout")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/saml/logout")

        self.set_user('javerage')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/5.0 MyUW_Hybrid/1.0")
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_user_not_in_pws(self):
        req = get_request_with_user('usernotinpws')
        response = page(req, 'index.html', add_quicklink_context=True)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(
            response.reason_phrase,
            ("<p>MyUW cannot find data for this user account "
             "in the Person Registry services. If you have just "
             "created your UW NetID, please try signing in to "
             "MyUW again in one hour.</p>"))

        url = reverse("myuw_home")
        self.set_user('usernotinpws')
        User.objects.create(uwnetid='usernotinpws', last_visit=timezone.now())
        response = self.client.get(url,
                                   HTTP_USER_AGENT="Mozilla/5.0")
        self.assertEquals(response.status_code, 403)
        self.assertEquals(
            response.reason_phrase,
            ('<p>MyUW cannot find data for this user account '
             'in the Person Registry services. Please contact the '
             '<a href="https://itconnect.uw.edu/it-connect-home/question/">'
             'UW-IT Service Center</a>.</p>'))

    @patch('myuw.views.page.get_updated_user', spec=True)
    def test_pws_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "pws err")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 500)

    @patch('myuw.views.page.get_card_visibilty_date_values', spec=True)
    def test_sws_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "sws err")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    @patch('myuw.views.page.can_access_myuw', spec=True)
    def test_gws_err_can_access_myuw(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "GWS err")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 500)

    @patch('myuw.views.page.get_all_affiliations', spec=True)
    def test_gws_err_get_all_affiliations(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "affi GWS err")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 500)

    @patch('myuw.views.page.get_service_url_for_address', spec=True)
    def test_email_forward_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = EmailServiceUrlException
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    @patch('myuw.views.page.prefetch_resources', spec=True)
    def test_prefetch_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "prefetch GWS err")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_blocked_netid(self):
        url = reverse("myuw_home")
        self.set_user('nobody')
        response = self.client.get(url,
                                   HTTP_USER_AGENT="Mozilla/5.0")
        self.assertEquals(response.status_code, 403)
        self.assertEquals(
            response.reason_phrase,
            ('<p>MyUW encountered a problem with your uwnetid, '
             'please contact the <a href="https://itconnect.uw.edu/'
             'it-connect-home/question/">UW-IT Service Center</a>.</p>'))
