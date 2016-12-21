from unittest2 import skipIf
from django.core.urlresolvers import reverse
from myuw.test.api import missing_url, MyuwApiTest


class TestDispatchErrorCases(MyuwApiTest):

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_javerage(self):
        url = reverse("myuw_book_api",
                      kwargs={'year': 2013,
                              'quarter': 'spring',
                              'summer_term': ''})
        self.set_user('javerage')
        response = self.client.put(url)
        self.assertEquals(response.status_code, 405)

        response = self.client.post(url)
        self.assertEquals(response.status_code, 405)

        response = self.client.delete(url)
        self.assertEquals(response.status_code, 405)
