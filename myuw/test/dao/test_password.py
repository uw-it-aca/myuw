# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from django.test import TestCase
from myuw.dao.password import (get_password_info, get_pw_json,
                               get_days_after, get_days_before)
from myuw.test import (get_request_with_date, get_request_with_user,
                       get_request, fdao_uwnetid_override)


@fdao_uwnetid_override
class TestDaoPassword(TestCase):

    def test_get_password_info(self):
        req = get_request_with_user('javerage')
        self.assertFalse(hasattr(req, "myuw_netid_password"))
        pw = get_password_info(req)
        self.assertIsNotNone(req.myuw_netid_password)

    def test_last_pw_change(self):
        now_request = get_request_with_date('2013-02-27')
        request = get_request_with_user('javerage', now_request)
        pw_json = get_pw_json(request)
        self.assertEqual(pw_json["days_after_last_pw_change"], 30)
        self.assertFalse(pw_json["has_active_med_pw"])

        now_request = get_request_with_date('2013-01-31')
        request = get_request_with_user('javerage', now_request)
        pw_json = get_pw_json(request)
        self.assertEqual(pw_json["days_after_last_pw_change"], 3)

    def test_last_med_pw_change(self):
        now_request = get_request_with_date('2013-05-05')
        request = get_request_with_user('staff', now_request)
        pw_json = get_pw_json(request)
        self.assertTrue(pw_json["has_active_med_pw"])
        self.assertFalse(pw_json["med_pw_expired"])
        self.assertEqual(pw_json["days_after_last_med_pw_change"], 90)
        self.assertEqual(pw_json["days_before_med_pw_expires"], 29)
        self.assertTrue(pw_json["expires_in_30_days_or_less"])

        now_request = get_request_with_date('2013-03-10')
        request = get_request_with_user('staff', now_request)
        pw_json = get_pw_json(request)
        self.assertFalse(pw_json["med_pw_expired"])
        self.assertEqual(pw_json["days_after_last_med_pw_change"], 34)
        self.assertEqual(pw_json["days_before_med_pw_expires"], 85)
        self.assertFalse(pw_json["expires_in_30_days_or_less"])

        now_request = get_request_with_date('2013-07-05')
        request = get_request_with_user('staff', now_request)
        pw_json = get_pw_json(request)
        self.assertTrue(pw_json["med_pw_expired"])
