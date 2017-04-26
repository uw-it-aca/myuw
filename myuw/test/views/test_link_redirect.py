from myuw.test.api import missing_url, require_url, MyuwApiTest
from myuw.models import VisitedLink
from django.core.urlresolvers import reverse
from django.test import Client


@require_url('myuw_home')
class TestRedirect(MyuwApiTest):

    def test_invalid_urls(self):
        VisitedLink.objects.all().delete()

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

        all = VisitedLink.objects.all()
        self.assertEquals(len(all), 0)

    def test_valid_urls(self):
        VisitedLink.objects.all().delete()

        self.set_user('javerage')
        url = reverse('myuw_outbound_link')
        response = self.client.get(url, {'u': 'https://example.com',
                                         'l': 'example'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "https://example.com")

        all = VisitedLink.objects.all()
        self.assertEquals(all[0].label, 'example')

        response = self.client.get(url, {'u': 'http://example.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://example.com")

        all = VisitedLink.objects.all()
        self.assertEquals(len(all), 2)

        self.set_user('jbothell')
        response = self.client.get(url, {'u': 'http://example.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://example.com")
        all = VisitedLink.objects.all()
        self.assertEquals(len(all), 3)

        pce = VisitedLink.objects.filter(is_seattle=True)
        self.assertEquals(len(pce), 2)

    def test_anonymous_user(self):
        VisitedLink.objects.all().delete()
        self.client.logout()
        url = reverse('myuw_outbound_link')
        response = self.client.get(url, {'u': 'https://example.com',
                                         'l': 'example'})

        all = VisitedLink.objects.all()
        self.assertEquals(len(all), 1)
        self.assertTrue(all[0].is_anonymous)
        self.assertEquals(all[0].username, "")
