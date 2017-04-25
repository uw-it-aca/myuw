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

        response = self.client.post(url, {'url': 'google.com'})
        self.assertEquals(response.status_code, 404)

        response = self.client.post(url, {'url': 'javascript:alert("OK");'})
        self.assertEquals(response.status_code, 404)

        response = self.client.post(url, {'url': 'data:,Hello%2C%20World!'})
        self.assertEquals(response.status_code, 404)

        w_http = 'javascript:alert("http://google.com")'
        response = self.client.post(url, {'url': w_http})
        self.assertEquals(response.status_code, 404)

        all = VisitedLink.objects.all()
        self.assertEquals(len(all), 0)

    def test_valid_urls(self):
        VisitedLink.objects.all().delete()

        self.set_user('javerage')
        url = reverse('myuw_outbound_link')
        response = self.client.post(url, {'url': 'http://google.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://google.com")

        response = self.client.post(url, {'url': 'https://google.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "https://google.com")

        all = VisitedLink.objects.all()
        self.assertEquals(len(all), 2)

        self.set_user('jbothell')
        response = self.client.post(url, {'url': 'http://google.com'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"], "http://google.com")
        all = VisitedLink.objects.all()
        self.assertEquals(len(all), 3)

        pce = VisitedLink.objects.filter(is_seattle=True)
        self.assertEquals(len(pce), 2)
