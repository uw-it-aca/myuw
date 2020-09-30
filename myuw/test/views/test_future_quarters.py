from unittest import skipIf
from django.urls import reverse
from myuw.test.api import MyuwApiTest, missing_url


class TestFutureQuarterPage(MyuwApiTest):

    @skipIf(missing_url("myuw_future_quarters_page",
                        kwargs={"quarter": "2013,summer,a-term"}),
            "myuw urls not configured")
    def test_student_summer_aterm(self):
        url = reverse("myuw_future_quarters_page",
                      kwargs={"quarter": "2013,summer,a-term"})
        self.set_user("javerage")
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['future_term'], "2013,summer,a-term")
        self.assertEqual(response.context['term_data']['summer_term'],
                         "a-term")
