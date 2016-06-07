from myuw.test.api import MyuwApiTest, require_url
import json


@require_url('myuw_profile_api')
class TestProfile(MyuwApiTest):

    def get_profile_response(self):
        return self.get_response_by_reverse('myuw_profile_api')

    def test_javerage(self):
        self.set_user('javerage')
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["first_name"], "John Joseph")
        self.assertEquals(data["last_name"], "Average")
        self.assertEquals(data["local_address"]["street_line1"],
                          "4634 26th Ave NE")
        self.assertEquals(data["local_address"]["zip_code"], "98105-4566")
        self.assertEquals(data["student_number"], "1033334")

    def test_jerror(self):
        self.set_user('jerror')
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 543)

        self.set_user('nouser')
        response = self.get_profile_response()
        self.assertEquals(response.status_code, 404)
