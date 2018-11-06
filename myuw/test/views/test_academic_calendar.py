from unittest import skipIf
from django.urls import reverse
from myuw.test.api import missing_url, MyuwApiTest


class TestAcademicsMethods(MyuwApiTest):

    @skipIf(missing_url("myuw_academic_calendar_page"),
            "myuw urls not configured")
    def test_student_access(self):
        url = reverse("myuw_academic_calendar_page")
        self.set_user('javerage')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEquals(response.status_code, 200)
