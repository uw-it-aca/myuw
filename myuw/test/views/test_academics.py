from unittest2 import skipIf
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from myuw.views.page import _is_mobile
from myuw.test.api import missing_url, MyuwApiTest


legacy_url = "http://some-test-server/myuw"


@override_settings(MYUW_USER_SERVLET_URL=legacy_url)
class TestAcademicsMethods(MyuwApiTest):

    @skipIf(missing_url("myuw_academics_page"), "myuw urls not configured")
    def test_student_access(self):
        url = reverse("myuw_academics_page")
        self.set_user('javerage')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEquals(response.status_code, 200)
