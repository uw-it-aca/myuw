# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from django.test import TestCase
from myuw.dao.password import get_password_info, get_pw_json
from myuw.test import get_request_with_user, fdao_uwnetid_override


@fdao_uwnetid_override
class TestDaoPassword(TestCase):

    def test_get_password_info(self):
        req = get_request_with_user('javerage')
        self.assertFalse(hasattr(req, "myuw_netid_password"))
        pw = get_password_info(req)
        self.assertIsNotNone(req.myuw_netid_password)

    def test_last_med_pw_change(self):
        request = get_request_with_user('staff')
        pw_json = get_pw_json(request)
        self.assertIsNotNone(pw_json["expires_med"])
