# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.test.api import missing_url, require_url, MyuwApiTest
from myuw.models import VisitedLinkNew
from django.urls import reverse
from django.test.utils import override_settings
from django.test import Client
from django.urls import reverse_lazy


@require_url('myuw_home')
@override_settings(LOGIN_URL=reverse_lazy('saml_login'))
class TestRedirect(MyuwApiTest):

    def test_invalid_urls(self):
        self.client.logout()
        url = reverse('myuw_outbound_link')

        response = self.client.get(url, {'u': 'example.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/saml/login?next=/"
                                                "out%3Fu%3Dexample.com")

        response = self.client.get(url,
                                   {'u': 'javascript:alert("OK");'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/saml/login?next=/out%3Fu%3D"
                                                "javascript%253Aalert%2528%25"
                                                "22OK%2522%2529%253B")

        response = self.client.get(url, {'u': 'data:,Hello%2C%20World!'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/saml/login?next=/out%3Fu%3D"
                                                "data%253A%252CHello%25252C%25"
                                                "2520World%2521")

        w_http = 'javascript:alert("http://example.com")'
        response = self.client.get(url, {'u': w_http})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/saml/login?next=/out%3Fu%3D"
                                                "javascript%253Aalert%2528%252"
                                                "2http%253A%252F%252Fexample."
                                                "com%2522%2529")

        all = VisitedLinkNew.objects.all()
        self.assertEquals(len(all), 0)

    def test_valid_urls(self):
        self.set_user('javerage')
        url = reverse('myuw_outbound_link')
        response = self.client.get(url, {'u': 'https://example.com',
                                         'l': 'example'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "https://example.com")

        all = VisitedLinkNew.objects.all()
        self.assertEquals(all[0].label, 'example')

        response = self.client.get(url, {'u': 'http://example.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://example.com")

        all = VisitedLinkNew.objects.all()
        self.assertEquals(len(all), 2)

        self.set_user('jbothell')
        response = self.client.get(url, {'u': 'http://example.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://example.com")
        all = VisitedLinkNew.objects.all()
        self.assertEquals(len(all), 3)

        pce = VisitedLinkNew.objects.filter(is_seattle=True)
        self.assertEquals(len(pce), 2)

    def test_anonymous_user(self):
        self.client.logout()
        url = reverse('myuw_outbound_link')
        response = self.client.get(url, {'u': 'https://example.com',
                                         'l': 'example'})

        all = VisitedLinkNew.objects.all()
        self.assertEquals(len(all), 0)

    def test_ignore_link(self):
        url = reverse('myuw_outbound_link')
        self.set_user('jbothell')
        response = self.client.get(url, {'u': 'http://gmail.uw.edu'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://gmail.uw.edu")
        all = VisitedLinkNew.objects.all()
        self.assertEquals(len(all), 0)
