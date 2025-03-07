# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
import json
from myuw.test.api import (
    MyuwApiTest, require_url, fdao_uw_admin_sys_override)


@fdao_uw_admin_sys_override
@require_url("myuw_idcard_elig_api")
class TestIDcardApi(MyuwApiTest):

    def test_normal(self):
        self.set_user('javerage')
        response = self.get_response_by_reverse('myuw_idcard_elig_api')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("UTF-8")),
            {
                "not_eligible": False,
                "employee_eligible": True,
                "student_eligible": True,
                "retiree_eligible": False,
            },
        )

    def test_error_404(self):
        self.set_user('noexist')
        response = self.get_response_by_reverse('myuw_idcard_elig_api')
        self.assertEqual(response.status_code, 404)
