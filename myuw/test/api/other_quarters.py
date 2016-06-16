import json
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_other_quarters_api')
class TestOtherQuarters(MyuwApiTest):

    def get_oquarters_response(self):
        return self.get_response_by_reverse('myuw_other_quarters_api')

    def test_javerage_oquarters(self):
        self.set_user('javerage')
        response = self.get_oquarters_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data["next_term_data"]["has_registration"], True)
        self.assertEquals(data["next_term_data"]["quarter"], "Autumn")
        self.assertEquals(data["next_term_data"]["year"], 2013)

        self.assertEquals(len(data["terms"]), 3)

        self.assertEquals(data["terms"][0]['section_count'], 2)
        self.assertEquals(data["terms"][0]['url'], '/2013,summer,a-term')
        self.assertEquals(data["terms"][0]['summer_term'], 'a-term')
        self.assertEquals(data["terms"][0]['year'], 2013)
        self.assertEquals(data["terms"][0]['quarter'], 'Summer')
        self.assertEquals(data["terms"][0]['credits'], '2.0')
        self.assertEquals(data["terms"][0]['last_final_exam_date'],
                          '2013-08-23 23:59:59')

    def test_error(self):
        self.set_user('jerror')
        response = self.get_oquarters_response()
        self.assertEquals(response.status_code, 543)

        self.set_user('nouser')
        response = self.get_oquarters_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data["terms"]), 0)
