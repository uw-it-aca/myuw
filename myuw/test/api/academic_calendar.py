from myuw.test.api import require_url, MyuwApiTest
import json


@require_url('myuw_home')
class TestCalendarAPI(MyuwApiTest):

    def get_cal(self):
        rev = 'myuw_academic_calendar'
        return self.get_response_by_reverse(rev)

    def get_cal_current(self):
        rev = 'myuw_academic_calendar_current'
        return self.get_response_by_reverse(rev)

    def test_all_events(self):
        self.set_user('javerage')
        response = self.get_cal()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 29)

        self.set_date('2013-04-18')

        response = self.get_cal()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 28)

    def test_muwm_2489(self):
        self.set_user('javerage')
        self.set_date('2013-05-30')
        response = self.get_cal_current()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 3)
        for event in data:
            self.assertNotEqual(event["summary"], "Memorial Day (no classes)")

    def test_current_events(self):
        self.set_user('javerage')
        response = self.get_cal_current()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 4)

        self.set_date('2013-04-18')
        response = self.get_cal_current()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 3)

    # Test a workaround for MUWM-2522
    def test_failing_term_resource(self):
        self.set_user('javerage')
        self.set_date('2013-07-25')
        response = self.get_cal()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertGreater(len(data), 1)
