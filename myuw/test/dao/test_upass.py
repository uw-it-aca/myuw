# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.upass import get_upass, in_summer_display_window
from myuw.test import fdao_upass_override, get_request_with_user,\
    get_request_with_date, fdao_sws_override, fdao_gws_override


@fdao_upass_override
@fdao_sws_override
@fdao_gws_override
class TestUPassDao(TestCase):

    def test_in_summer_display_window(self):
        req = get_request_with_date("2013-06-07 00:00:00")
        self.assertFalse(in_summer_display_window(req))
        req = get_request_with_date("2013-06-07 00:00:01")
        self.assertTrue(in_summer_display_window(req))
        req = get_request_with_date("2013-06-24")
        self.assertTrue(in_summer_display_window(req))
        req = get_request_with_date("2013-09-17 23:59:59")
        self.assertTrue(in_summer_display_window(req))
        req = get_request_with_date("2013-09-18 00:00:00")
        self.assertFalse(in_summer_display_window(req))

    def test_get_by_netid(self):
        req = get_request_with_user("javerage",
                                    get_request_with_date("2013-06-06"))
        status = get_upass(req)
        self.assertEqual(status, {
            'active_employee_membership': True,
            'active_student_membership': True,
            'in_summer': False})
        req = get_request_with_user("javerage",
                                    get_request_with_date("2013-06-07"))
        status = get_upass(req)
        self.assertTrue(status['in_summer'])

        req = get_request_with_user("javerage",
                                    get_request_with_date("2013-07-07"))
        status = get_upass(req)
        self.assertTrue(status['in_summer'])

        req = get_request_with_user("javerage",
                                    get_request_with_date("2013-09-17"))
        status = get_upass(req)
        self.assertTrue(status['in_summer'])

        req = get_request_with_user("javerage",
                                    get_request_with_date("2013-09-18"))
        status = get_upass(req)
        self.assertFalse(status['in_summer'])

        req = get_request_with_user("none")
        status = get_upass(req)
        self.assertEqual(status, {
            'active_employee_membership': None,
            'active_student_membership': None})

        req = get_request_with_user("jerror")
        self.assertRaises(Exception, get_upass, req)
