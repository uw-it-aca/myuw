import json
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_email_api')
class TestUWEmail(MyuwApiTest):

    def get_email_response(self):
        return self.get_response_by_reverse('myuw_email_api')

    def test_javerage_email(self):
        self.set_user('javerage')
        response = self.get_email_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data["status"], "Active")
        self.assertEquals(data["fwd"], "javerage@gamail.uw.edu")
        self.assertTrue(data["is_active"])
        self.assertFalse(data["is_uwlive"])
        self.assertTrue(data["is_uwgmail"])
        self.assertTrue(data["permitted"])

    def test_error(self):
        self.set_user('jerror')
        response = self.get_email_response()
        self.assertEquals(response.status_code, 543)

        self.set_user('nouser')
        response = self.get_email_response()
        self.assertEquals(response.status_code, 404)
