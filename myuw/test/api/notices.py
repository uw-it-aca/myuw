from myuw.test.api import MyuwApiTest, require_url
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
import json


@require_url('myuw_notices_api')
class TestNotices(MyuwApiTest):

    def get_notices_response(self):
        return self.get_response_by_reverse('myuw_notices_api')

    def put_notice(self, data):
        url = reverse('myuw_notices_api')
        return self.client.put(url, data)

    def test_javerage_notices(self):
        self.set_user('javerage')
        response = self.get_notices_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 23)
        self.assertFalse(data[0]["is_read"])

        hash_value = data[0]["id_hash"]

        response = self.put_notice('{"notice_hashes":["%s"]}' % hash_value)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '')

        response = self.get_notices_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 23)

        match = False
        for el in data:
            if el["id_hash"] == hash_value:
                match = True
                self.assertEquals(el["is_read"], True)

        self.assertEquals(match, True)

        response = self.put_notice('{"notice_hashes":["fake-fake-fake"]}')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '')

    def test_error_cases(self):
        self.set_user('jerror')
        response = self.get_notices_response()
        self.assertEquals(response.status_code, 543)

        self.set_user('staff')
        response = self.get_notices_response()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

    def test_est_reg_date(self):
        self.set_user('jinter')
        self.set_date('2013-05-09 23:59:59')
        response = self.get_notices_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 31)
        for el in data:
            if el["category"] == "Registration" and\
                    'est_reg_date' in el["location_tags"]:
                self.assertFalse(el["is_my_1st_reg_day"])
                self.assertFalse(el["my_reg_has_opened"])

        self.set_date('2013-05-10 00:00:01')
        response = self.get_notices_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 31)
        for el in data:
            if el["category"] == "Registration" and\
                    'est_reg_date' in el["location_tags"]:
                self.assertTrue(el["is_my_1st_reg_day"])
                self.assertTrue(el["my_reg_has_opened"])

        self.set_user('jbothell')
        self.set_date('2014-02-14 00:00:01')
        response = self.get_notices_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 14)
        for el in data:
            if el["category"] == "Registration" and\
                    'est_reg_date' in el["location_tags"]:
                self.assertTrue(el["is_my_1st_reg_day"])
                self.assertTrue(el["my_reg_has_opened"])
