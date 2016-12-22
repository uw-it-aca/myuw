from datetime import datetime
from django.test import TestCase
from myuw.dao.password import (get_password_info, get_pw_json,
                               get_days_after_last_change,
                               get_days_before_expires)
from myuw.test import (get_request_with_date, get_request_with_user,
                       get_request, fdao_uwnetid_override)


@fdao_uwnetid_override
class TestDaoPassword(TestCase):
    def setUp(self):
        get_request()

    def test_last_pw_change(self):
        now_request = get_request_with_date('2013-02-27')
        request = get_request_with_user('javerage', now_request)
        pw_json = get_pw_json("javerage", request)
        self.assertEqual(pw_json["days_after_last_pw_change"], 30)

        now_request = get_request_with_date('2013-01-31')
        request = get_request_with_user('javerage', now_request)
        pw_json = get_pw_json("javerage", request)
        self.assertEqual(pw_json["days_after_last_pw_change"], 3)

    def test_last_med_pw_change(self):
        now_request = get_request_with_date('2014-01-11')
        request = get_request_with_user('staff', now_request)
        pw_json = get_pw_json("staff", request)
        self.assertEqual(pw_json["days_after_last_med_pw_change"], 89)
        self.assertEqual(pw_json["days_before_med_pw_expires"], 30)
        self.assertTrue(pw_json["expires_in_30_days_or_less"])

        now_request = get_request_with_date('2014-01-10')
        request = get_request_with_user('staff', now_request)
        pw_json = get_pw_json("staff", request)
        self.assertEqual(pw_json["days_after_last_med_pw_change"], 88)
        self.assertEqual(pw_json["days_before_med_pw_expires"], 31)
        self.assertFalse(pw_json["expires_in_30_days_or_less"])
