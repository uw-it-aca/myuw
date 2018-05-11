from unittest2 import skipIf
from django.core.urlresolvers import reverse
from django.test import Client
from myuw.views.link_admin import popular_links
from myuw.test.api import missing_url, require_url, MyuwApiTest


@require_url('myuw_popular_links')
class TestViewsLinkAdmin(MyuwApiTest):

    @skipIf(missing_url("myuw_popular_links"),
            "myuw_popular_links urls not configured")
    def test_popular_links(self):
        url = reverse("myuw_popular_links",
                      kwargs={'page': 1})
        self.set_user('javerage')
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

    @skipIf(missing_url("myuw_popular_links"),
            "myuw_popular_links urls not configured")
    def test_login_required_decorator(self):
        self.client.logout()
        url = reverse("myuw_popular_links",
                      kwargs={'page': 1})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response["Location"],
                          '/accounts/login/?next=/admin/links')

    @skipIf(missing_url("myuw_popular_links"),
            "myuw_popular_links urls not configured")
    def test_admin_required_decorator(self):
        self.set_user('none')
        url = reverse("myuw_popular_links",
                      kwargs={'page': 1})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        not_authorized = "<title>403 Error: Access Denied</title>"
        self.assertTrue(not_authorized in str(response.content))
