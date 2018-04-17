from myuw.test.api import missing_url, require_url, MyuwApiTest
from myuw.models import VisitedLinkNew
from django.core.urlresolvers import reverse
from django.test import Client


@require_url('myuw_home')
class TestRedirect(MyuwApiTest):

    def test_invalid_urls(self):
        self.client.logout()
        url = reverse('myuw_outbound_link')

        response = self.client.get(url, {'u': 'example.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/")

        response = self.client.get(url,
                                   {'u': 'javascript:alert("OK");'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/")

        response = self.client.get(url, {'u': 'data:,Hello%2C%20World!'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/")

        w_http = 'javascript:alert("http://example.com")'
        response = self.client.get(url, {'u': w_http})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "/")

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
