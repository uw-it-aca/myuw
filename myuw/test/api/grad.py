from datetime import datetime
from myuw.test.api import MyuwApiTest, require_url, fdao_grad_override
import json


@fdao_grad_override
@require_url('myuw_grad_api')
class TestApiGrad(MyuwApiTest):

    def test_javerage(self):
        self.set_user('seagrad')
        response = self.get_response_by_reverse('myuw_grad_api')
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.content)
        data = json.loads(response.content)

        self.assertIn('degrees', data)
        self.assertEquals(len(data["degrees"]), 8)
        degree = data["degrees"][0]
        self.assertEqual(degree["req_type"], "Masters Request")
        self.assertEqual(degree["submit_date"], "2013-03-11T20:53:32")
        self.assertEqual(
            degree["degree_title"],
            "Master Of Landscape Architecture/Master Of Architecture")
        self.assertEqual(degree["major_full_name"],
                         "Landscape Arch/Architecture (Concurrent)")
        self.assertEqual(degree["status"],
                         "Awaiting Dept Action")
        self.assertIsNone(degree["exam_place"])
        self.assertIsNone(degree["exam_date"])
        self.assertEqual(degree["target_award_year"], 2013)
        self.assertEqual(degree["target_award_quarter"], "Spring")
        # committees
        self.assertIsNotNone(data.get("committees"))
        self.assertEquals(len(data["committees"]), 3)
        committee = data["committees"][0]
        self.assertEqual(committee['committee_type'], "Advisor")
        self.assertEqual(committee['status'], "active")
        self.assertEqual(committee['dept'], "Anthropology")
        self.assertEqual(committee['degree_title'], None)
        self.assertEqual(committee['degree_type'],
                         "Master Of Public Health (Epidemiology)")
        self.assertEqual(committee['major_full_name'], "ANTH")
        self.assertEqual(committee['start_date'],
                         "2012-12-07T08:26:14")
        self.assertEqual(len(committee['members']), 1)
        # leaves
        self.assertIsNotNone(data.get("leaves"))
        self.assertEquals(len(data["leaves"]), 3)
        leave = data["leaves"][0]
        self.assertEqual(leave['reason'],
                         "Dissertation/Thesis research/writing")
        self.assertEqual(leave['submit_date'],
                         "2012-09-10T09:40:03")
        self.assertEqual(leave['status'], "Requested")
        self.assertEqual(len(leave['terms']), 1)
        self.assertEqual(leave['terms'][0]['quarter'], "Spring")
        self.assertEqual(leave['terms'][0]['year'], 2013)
        # petitions
        self.assertIsNotNone(data.get("petitions"))
        self.assertEquals(len(data["petitions"]), 7)
        petition = data["petitions"][6]
        self.assertEqual(petition['description'],
                         "Doctoral degree - Extend ten year limit")
        self.assertEqual(petition['submit_date'],
                         "2013-04-06T16:32:28")
        self.assertEqual(petition['decision_date'],
                         "2013-04-10T00:00:00")
        self.assertEqual(petition['dept_recommend'], "Approve")
        self.assertEqual(petition['gradschool_decision'], "Approved")

    def test_error(self):
        self.set_user('none')
        response = self.get_response_by_reverse('myuw_grad_api')
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.content, 'Data not found')

        self.set_user('jerror')
        response = self.get_response_by_reverse('myuw_grad_api')
        self.assertEquals(response.status_code, 543)
