# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import (
    MyuwApiTest, require_url, fdao_pws_override,
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
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["uwnetid"], 'javerage')
        self.assertEqual(data["display_name"], "J. Average Student")
        self.assertEqual(data["first_name"], "John Joseph")
        self.assertEqual(data["last_name"], "Average")
        self.assertEqual(data["local_address"]["street_line1"],
                         "4634 26th Ave NE")
        self.assertEqual(data["local_address"]["zip_code"], "98105-4566")
        self.assertEqual(data["student_number"], "1033334")

        self.assertEqual(data["campus"], "Seattle")
        self.assertEqual(data["class_level"], "SENIOR")
        self.assertEqual(len(data["term_majors"]), 4)
        self.assertEqual(len(data["term_minors"]), 4)
        pw_data = data["password"]
        self.assertEqual(pw_data["last_change"],
                         "2013-01-27 10:49:42-08:00")
        self.assertIsNone(pw_data["last_change_med"])
        self.assertIsNone(pw_data["expires_med"])

    def test_bothell_student(self):
        response = self.get_profile_response("jbothell")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["campus"], "Bothell")
        self.assertEqual(data["uwnetid"], "jbothell")
        pw_data = data["password"]
        self.assertIsNotNone(pw_data["last_change"])

    def test_tacoma_student(self):
        response = self.get_profile_response("eight")
        data = json.loads(response.content)
        self.assertEqual(data["uwnetid"], "eight")
        self.assertEqual(data["campus"], "Tacoma")
        pw_data = data["password"]
        self.assertIsNotNone(pw_data["last_change"])

    def test_password(self):
        response = self.get_profile_response("staff", adate="2014-01-10")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["uwnetid"], "staff")
        pw_data = data["password"]
        self.assertTrue(pw_data["last_change"])
        self.assertTrue(pw_data["expires_med"])

    def test_error_cases(self):
        response = self.get_profile_response("jerror")
        self.assertEqual(response.status_code, 543)

        response = self.get_profile_response("nouser")
        self.assertEqual(response.status_code, 404)

        response = self.get_profile_response('none')
        self.assertEqual(response.status_code, 200)

    def test_change_majors_once(self):
        response = self.get_profile_response('javg001')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn("term_majors", data)
        self.assertFalse(data['term_majors'][0]['degrees_modified'])
        self.assertTrue(data['term_majors'][1]['degrees_modified'])
        self.assertFalse(data['term_majors'][2]['degrees_modified'])

        self.assertEqual(len(data['term_majors'][0]['majors']), 1)
        self.assertEqual(len(data['term_majors'][1]['majors']), 2)
        self.assertEqual(len(data['term_majors'][2]['majors']), 2)

    def test_summer_major_only(self):
        # test to see if modified works
        response = self.get_profile_response('eight')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn("term_majors", data)
        self.assertEqual(len(data['term_majors'][0]['majors']), 2)
        self.assertEqual(len(data['term_majors'][1]['majors']), 3)
        self.assertEqual(len(data['term_majors'][2]['majors']), 2)

        self.assertFalse(data['term_majors'][0]['degrees_modified'])
        self.assertTrue(data['term_majors'][1]['degrees_modified'])
        self.assertTrue(data['term_majors'][2]['degrees_modified'])

    def test_change_once_and_add_another(self):
        response = self.get_profile_response('javg002')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn("term_majors", data)
        self.assertFalse(data['term_majors'][0]['degrees_modified'])
        self.assertTrue(data['term_majors'][1]['degrees_modified'])
        self.assertTrue(data['term_majors'][2]['degrees_modified'])
        self.assertFalse(data['term_majors'][3]['degrees_modified'])

        self.assertEqual(len(data['term_majors'][0]['majors']), 1)
        self.assertEqual(len(data['term_majors'][1]['majors']), 1)
        self.assertEqual(len(data['term_majors'][2]['majors']), 2)
        self.assertEqual(len(data['term_majors'][3]['majors']), 2)

    def test_drop_major(self):
        response = self.get_profile_response('javg003')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn("term_majors", data)
        self.assertFalse(data['term_majors'][0]['degrees_modified'])
        self.assertTrue(data['term_majors'][1]['degrees_modified'])
        self.assertFalse(data['term_majors'][2]['degrees_modified'])
        self.assertFalse(data['term_majors'][3]['degrees_modified'])

        self.assertEqual(len(data['term_majors'][0]['majors']), 2)
        self.assertEqual(len(data['term_majors'][1]['majors']), 1)
        self.assertEqual(len(data['term_majors'][2]['majors']), 1)
        self.assertEqual(len(data['term_majors'][3]['majors']), 1)

    def test_no_major_or_minor(self):
        response = self.get_profile_response('javg004')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertTrue("term_majors" in data)
        self.assertEqual(len(data['term_majors']), 2)
        self.assertEqual(len(data['term_majors'][0]['majors']), 0)
        self.assertEqual(len(data['term_majors'][1]['majors']), 0)

        self.assertIn("term_minors", data)
        self.assertEqual(len(data['term_minors']), 2)
        self.assertEqual(len(data['term_minors'][0]['minors']), 0)
        self.assertEqual(len(data['term_minors'][1]['minors']), 0)

    def test_drop_minor(self):
        response = self.get_profile_response('javg002')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn("term_minors", data)
        self.assertFalse(data['term_minors'][0]['degrees_modified'])

        self.assertEqual(len(data['term_minors']), 4)
        self.assertEqual(len(data['term_minors'][0]['minors']), 1)
        self.assertEqual(len(data['term_minors'][1]['minors']), 0)

    def test_no_pending(self):
        response = self.get_profile_response('javg005')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertFalse(data['has_pending_major'])
        self.assertFalse(data['has_pending_minor'])
        majors = data['term_majors']
        minors = data['term_minors']

        for major in majors:
            self.assertFalse(major['degrees_modified'])

        for minor in minors:
            self.assertFalse(minor['degrees_modified'])

    def test_degree_status(self):
        # MUWM-5010
        response = self.get_profile_response('javg004')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        degrees = data['degree_status']['degrees']
        self.assertTrue(degrees[0]["is_degree_earned_term"])
        self.assertTrue(degrees[0]["during_april_may"])
        self.assertTrue(degrees[1]["before_degree_earned_term"])
        self.assertTrue(degrees[1]["during_april_may"])

    def test_applicant_profile(self):
        response = self.get_profile_response('japplicant')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['email'], 'japplicant@u.washington.edu')
        self.assertNotIn("term_majors", data)
