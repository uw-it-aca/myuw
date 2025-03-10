# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.idcard_elig import get_idcard_eli
from myuw.test import (
    fdao_uw_admin_sys_override, get_request_with_user)


@fdao_uw_admin_sys_override
class TestIDcardDao(TestCase):

    def test_get_idcard_eli(self):
        req = get_request_with_user("javerage")
        status = get_idcard_eli(req)
        self.assertEqual(status, {
            "not_eligible": False,
            "employee_eligible": True,
            "student_eligible": True,
            "retiree_eligible": False})

        req = get_request_with_user("jpce")
        status = get_idcard_eli(req)
        self.assertEqual(status, {
            "not_eligible": True,
            "employee_eligible": False,
            "student_eligible": False,
            "retiree_eligible": False})
