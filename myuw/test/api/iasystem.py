import datetime
import pytz
import json
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_iasystem_api', message='IAS urls not configured')
class TestIasystemApi(MyuwApiTest):

    def get_ias_response(self):
        return self.get_response_by_reverse('myuw_iasystem_api')

    def test_javerage_normal_cases(self):
        response = self.get_ias_response()
        self.assertEquals(response.status_code, 302)

        self.set_user('javerage')
        response = self.get_ias_response()
        self.assertEquals(response.status_code, 404)

        # after show date 2013 Spring
        self.set_date('2013-05-31')
        response = self.get_ias_response()
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 5)

        # before show date
        self.set_date('2013-07-16')
        response = self.get_ias_response()
        self.assertEquals(response.status_code, 404)

        # after show date
        self.set_date('2013-07-17')
        response = self.get_ias_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Summer')
        self.assertEquals(len(data["sections"]), 2)
        eval_data = data["sections"][0]["evaluation_data"]
        self.assertEquals(len(eval_data), 0)
        eval_data = data["sections"][1]["evaluation_data"]
        self.assertEquals(len(eval_data), 0)

    def test_eight_2013_spring(self):
        self.set_user('eight')
        self.set_date('2013-06-08')
        response = self.get_ias_response()

        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 8)

    def test_user_none(self):
        self.set_user('none')
        response = self.get_ias_response()
        self.assertEquals(response.status_code, 404)

    def test_missing_current_term(self):
        self.set_user('err_user')
        response = self.get_ias_response()
        self.assertEquals(response.status_code, 404)

    def test_summer_terms(self):
        self.set_user('javerage')
        self.set_date('2013-07-24')
        response = self.get_ias_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Summer')
        self.assertEquals(data["summer_term"], "a-term")
        self.assertEquals(len(data["sections"]), 2)

        eval_data = data["sections"][0]["evaluation_data"]
        self.assertEquals(len(eval_data), 1)
        self.assertEquals(eval_data[0]['close_date'],
                          "2013-07-29 06:59:59 UTC+0000")

        eval_data = data["sections"][1]["evaluation_data"]
        self.assertEquals(len(eval_data), 0)

        self.set_date('2013-08-27')
        response = self.get_ias_response()

        data = json.loads(response.content)
        self.assertEquals(data["summer_term"], "b-term")
        self.assertEquals(len(data["sections"]), 2)

        eval_data = data["sections"][0]["evaluation_data"]
        self.assertEquals(len(eval_data), 0)

        eval_data = data["sections"][1]["evaluation_data"]
        self.assertEquals(len(eval_data), 1)
        self.assertEquals(eval_data[0]['close_date'],
                          "2013-08-29 06:59:59 UTC+0000")
