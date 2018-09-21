from unittest import skipIf
from django.test.utils import override_settings
from django.urls import reverse
from django.test.client import RequestFactory
from myuw.test.api import missing_url, MyuwApiTest


legacy_url = "http://some-test-server/myuw"


@override_settings(MYUW_USER_SERVLET_URL=legacy_url)
class TestViewsIndex(MyuwApiTest):

    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_student_access(self):
        url = reverse("myuw_home")
        self.set_user('javerage')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # self.assertEqual(len(response.context['popular_links']), 0)
        # self.assertEqual(len(response.context['recent_links']), 0)
        # self.assertEqual(response.context['default_links'][0],
        #                  {'url': 'http://canvas.uw.edu/',
        #                   'label': 'Canvas LMS'})
        self.assertTrue(len(response.context['card_display_dates']) > 0)
