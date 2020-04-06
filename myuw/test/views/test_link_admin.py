from unittest import skipIf
from django.urls import reverse
from django.test import Client
from django.test.utils import override_settings
from myuw.views.link_admin import popular_links
from myuw.test.api import missing_url, require_url, MyuwApiTest
from django.urls import reverse_lazy


@require_url('myuw_popular_links')
@override_settings(LOGIN_URL=reverse_lazy('saml_login'))
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
                          '/saml/login?next=/admin/links')

    @skipIf(missing_url("myuw_popular_links"),
            "myuw_popular_links urls not configured")
    def test_admin_required_decorator(self):
        self.set_user('none')
        url = reverse("myuw_popular_links",
                      kwargs={'page': 1})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 403)
