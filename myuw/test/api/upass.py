from datetime import datetime
import json
from myuw.test.api import MyuwApiTest, require_url, fdao_upass_override,\
    fdao_sws_override, fdao_gws_override


@fdao_upass_override
@fdao_sws_override
@fdao_gws_override
@require_url('myuw_upass_api')
class TestUpassApi(MyuwApiTest):

    def test_normal(self):
        self.set_user('seagrad')
        self.set_date("2013-04-1")
        response = self.get_response_by_reverse('myuw_upass_api')
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.content)
        data = json.loads(response.content)
        self.assertIn('status_message', data)
        self.assertTrue(data["is_current"])
        self.assertTrue(data["is_student"])
        self.assertTrue(data["display_activation"])
        self.assertFalse(data["is_employee"])
        self.assertFalse(data["in_summer"])

    def test_error_543(self):
        self.set_user('jerror')
        response = self.get_response_by_reverse('myuw_upass_api')
        self.assertEquals(response.status_code, 543)

    def test_error_404(self):
        self.set_user('none')
        response = self.get_response_by_reverse('myuw_upass_api')
        self.assertEquals(response.status_code, 404)
