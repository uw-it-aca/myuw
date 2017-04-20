import json
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_message_api')
class TestMessages(MyuwApiTest):

    def get_message_api_response(self):
        return self.get_response_by_reverse('myuw_message_api')

    def test_javerage(self):
        self.set_user('javerage')
        response = self.get_message_api_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['title'], "Test SERU Alert")

    def test_bad_user(self):
        self.set_user('err-user')
        response = self.get_message_api_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 0)
