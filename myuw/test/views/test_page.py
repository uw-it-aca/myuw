# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

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
        self.assertEqual(response.status_code, 403)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_desktop_redirect(self):
        url = reverse("myuw_home")
        self.set_user('javerage')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEqual(response.status_code, 200)

        self.set_user('faculty')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/4.0 (compatible; MSIE 5.01; WebISOGet")
        self.assertEqual(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_undergrad_access(self):
        url = reverse("myuw_home")
        self.set_user('jbothell')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_access(self):
        with self.settings(
                MYUW_SKIP_ACCESS_CHECK=False,
                MYUW_TEST_ACCESS_GROUP='u_astratst_myuw_test-support-admin'):
            url = reverse("myuw_home")
            self.set_user('jbothell')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)

            self.set_user('bill')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        with self.settings(
                MYUW_SKIP_ACCESS_CHECK=True,
                MYUW_TEST_ACCESS_GROUP='u_astratst_myuw_test-support-admin'):
            # MUWM-4710
            url = reverse("myuw_home")
            self.set_user('jbothell')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_support_links(self):
        url = reverse("myuw_date_override")
        self.set_user('jbothell')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_non_student_mobile(self):
        url = reverse("myuw_home")
        self.set_user('faculty')
        response = self.client.get(
            url,
            HTTP_USER_AGENT='Fake iPhone Agent')
        self.assertEqual(response.status_code, 200)

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
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["display_onboard_message"],
                             True)
            self.assertEqual(response.context["display_pop_up"], True)
            self.assertEqual(response.context["disable_actions"], False)
            self.assertIsNotNone(response.context["card_display_dates"])
            self.assertIsNotNone(response.context["user"]["affiliations"])
            self.assertIsNotNone(response.context["banner_messages"])
            self.assertEqual(response.context["user"]['email_forward_url'],
                             'http://alpine.washington.edu')
            self.assertIsNone(response.context['google_search_key'])
            self.assertIsNotNone(response.context['enabled_features'])

            self.set_user('billpce')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            self.set_user('billseata')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_no_user_in_session(self):
        # MUWM-4366
        url = reverse("myuw_home")
        login_url = reverse("saml_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{login_url}?next={url}")

    def test_logout(self):
        self.set_user('javerage')
        url = reverse("myuw_logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("saml_logout"))

        self.set_user('javerage')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Mozilla/5.0 MyUW_Hybrid/1.0")
        self.assertEqual(response.status_code, 200)

    @patch('myuw.views.page.get_updated_user', spec=True)
    def test_pws_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "pws err")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)

    @patch('myuw.views.page.get_card_visibilty_date_values', spec=True)
    def test_sws_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "sws err")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch('myuw.views.page.can_access_myuw', spec=True)
    def test_gws_err_can_access_myuw(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "GWS err")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)

    @patch('myuw.views.page.get_all_affiliations', spec=True)
    def test_gws_err_get_all_affiliations(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "affi GWS err")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)

    @patch('myuw.views.page.get_service_url_for_address', spec=True)
    def test_email_forward_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = EmailServiceUrlException
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch('myuw.views.page.prefetch_resources', spec=True)
    def test_prefetch_err(self, mock):
        url = reverse("myuw_home")
        self.set_user('javerage')
        mock.side_effect = DataFailureException(None, 500, "prefetch GWS err")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_blocked_netid(self):
        url = reverse("myuw_home")
        self.set_user('nobody')
        response = self.client.get(url,
                                   HTTP_USER_AGENT="Mozilla/5.0")
        self.assertEqual(response.status_code, 400)
