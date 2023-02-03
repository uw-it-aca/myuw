# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

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
        self.set_user('javerage')
        response = self.get_response_by_reverse('myuw_upass_api')
        self.assertEquals(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode('UTF-8')),
            {
                'active_employee_membership': True,
                'active_student_membership': True,
                'in_summer': False
            })

    def test_error_543(self):
        self.set_user('jerror')
        response = self.get_response_by_reverse('myuw_upass_api')
        self.assertEquals(response.status_code, 543)

    def test_error_404(self):
        self.set_user('noexist')
        response = self.get_response_by_reverse('myuw_upass_api')
        self.assertEquals(response.status_code, 404)
