import json
from myuw.test.api import MyuwApiTest, require_url, fdao_hfs_override


@fdao_hfs_override
@require_url('myuw_hfs_api')
class TestHFS(MyuwApiTest):

    def get_hfs_api_response(self):
        return self.get_response_by_reverse('myuw_hfs_api')

    def test_javerage(self):
        self.set_user('javerage')
        response = self.get_hfs_api_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(data["employee_husky_card"]["balance"], 1)
        self.assertEquals(data["resident_dining"]["balance"], 5.1)
        self.assertEquals(data["student_husky_card"]["balance"], 1.23)

    def test_bad_user(self):
        self.set_user('err-user')
        response = self.get_hfs_api_response()
        self.assertEquals(response.status_code, 404)

        self.set_user('none')
        response = self.get_hfs_api_response()
        self.assertEquals(response.status_code, 404)

    def test_error(self):
        self.set_user('jerror')
        response = self.get_hfs_api_response()
        self.assertEquals(response.status_code, 543)

    def test_eight(self):
        self.set_user('eight')
        response = self.get_hfs_api_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertIsNone(data["employee_husky_card"])
        self.assertEquals(data["resident_dining"]["balance"], 15.1)
        self.assertEquals(data["student_husky_card"]["balance"], 100.23)
