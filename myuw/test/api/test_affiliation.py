# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import MyuwApiTest, require_url


class TestApiAffiliation(MyuwApiTest):

    @require_url('myuw_affiliation')
    def test_javerage(self):
        self.set_user('fffjjj')
        response = self.get_response_by_reverse('myuw_affiliation')
        self.assertEquals(response.status_code, 403)

        self.set_user('javerage')
        response = self.get_response_by_reverse('myuw_affiliation')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["class_level"], "SENIOR")
        self.assertFalse(data["instructor"])
        self.assertFalse(data["applicant"])
        self.assertFalse(data["grad"])
        self.assertFalse(data["grad_c2"])
        self.assertFalse(data["undergrad_c2"])
        self.assertFalse(data["employee"])
        self.assertFalse(data["faculty"])
        self.assertFalse(data["clinician"])
        self.assertFalse(data["staff_employee"])
        self.assertFalse(data["bothell"])
        self.assertFalse(data["tacoma"])
        self.assertFalse(data["F1"])
        self.assertFalse(data["J1"])
        self.assertFalse(data["intl_stud"])
        self.assertFalse(data["grad"])
        self.assertFalse(data["alum_asso"])
        self.assertFalse(data["alumni"])
        self.assertFalse(data["retiree"])
        self.assertFalse(data["past_employee"])
        self.assertFalse(data["past_stud"])
        self.assertFalse(data["no_1st_class_affi"])
        self.assertFalse(data["official_bothell"])
        self.assertFalse(data["official_tacoma"])
        self.assertTrue(data["undergrad"])
        self.assertTrue(data["registered_stud"])
        self.assertTrue(data["pce"])
        self.assertTrue(data["stud_employee"])
        self.assertTrue(data["seattle"])
        self.assertTrue(data["official_seattle"])
        self.assertTrue(data["hxt_viewer"])
        self.assertTrue(data["enrolled_stud"])
        self.assertTrue(data["2fa_permitted"])
        self.assertEqual(self.request.session.get_expiry_age(), 60)
