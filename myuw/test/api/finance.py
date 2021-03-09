from myuw.test.api import MyuwApiTest, require_url
from datetime import datetime
import json


@require_url('myuw_finance_api')
class TestFinance(MyuwApiTest):

    def test_javerage(self):
        self.set_user('javerage')
        response = self.get_response_by_reverse('myuw_finance_api')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data['tuition_accbalance'], '12345.00')
        self.assertEquals(data['pce_accbalance'], '1000.00')

    def test_errors(self):
        self.set_user('jerror')
        response = self.get_response_by_reverse('myuw_finance_api')
        self.assertEquals(response.status_code, 543)

        self.set_user('staff')
        response = self.get_response_by_reverse('myuw_finance_api')
        self.assertEquals(response.status_code, 404)
