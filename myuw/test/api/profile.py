import json
from myuw.test.api import (MyuwApiTest, require_url, fdao_pws_override,
                           fdao_sws_override, fdao_uwnetid_override)


@fdao_sws_override
@fdao_pws_override
@fdao_uwnetid_override
@require_url('myuw_profile_api')
class TestProfile(MyuwApiTest):

    def get_profile_response(self, netid, adate=None):
        self.set_user(netid)
        if adate is not None:
            self.set_date(adate)
        return self.get_response_by_reverse('myuw_profile_api')

    def test_seattle_student(self):
        response = self.get_profile_response('javerage')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["uwnetid"], 'javerage')
        self.assertEquals(data["display_name"], "J. Average Student")
        self.assertEquals(data["first_name"], "John Joseph")
        self.assertEquals(data["last_name"], "Average")
        self.assertEquals(data["local_address"]["street_line1"],
                          "4634 26th Ave NE")
        self.assertEquals(data["local_address"]["zip_code"], "98105-4566")
        self.assertEquals(data["student_number"], "1033334")

        self.assertEquals(data["campus"], "Seattle")
        self.assertEquals(data["class_level"], "SENIOR")
        self.assertEquals(len(data["majors"]), 1)
        self.assertEquals(len(data["minors"]), 1)
        self.assertFalse(data["is_grad_student"])
        pw_data = data["password"]
        self.assertEquals(pw_data["last_change"],
                          "2013-01-27 10:49:42-08:00")
        self.assertFalse(pw_data["has_active_med_pw"])
        self.assertIsNone(pw_data["last_change_med"])
        self.assertIsNone(pw_data["expires_med"])

    def test_bothell_student(self):
        response = self.get_profile_response("jbothell")
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["campus"], "Bothell")
        self.assertEqual(data["uwnetid"], "jbothell")
        pw_data = data["password"]
        self.assertFalse(pw_data["has_active_med_pw"])

    def test_tacoma_student(self):
        response = self.get_profile_response("eight")
        data = json.loads(response.content)
        self.assertEqual(data["uwnetid"], "eight")
        self.assertEquals(data["campus"], "Tacoma")
        pw_data = data["password"]
        self.assertTrue(pw_data["has_active_med_pw"])

    def test_staff(self):
        response = self.get_profile_response("staff", adate="2014-01-10")
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["uwnetid"], "staff")
        self.assertFalse(data["is_student"])
        self.assertFalse(data["is_grad_student"])
        pw_data = data["password"]
        self.assertTrue(pw_data["has_active_med_pw"])
        self.assertTrue(pw_data["med_pw_expired"])

    def test_error_cases(self):
        response = self.get_profile_response("jerror")
        self.assertEquals(response.status_code, 543)

        response = self.get_profile_response("nouser")
        self.assertEquals(response.status_code, 404)

        response = self.get_profile_response('none')
        self.assertEquals(response.status_code, 200)
