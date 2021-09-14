# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.upass import get_upass, around_qtr_begin,\
    in_summer_display_window
from myuw.test import fdao_upass_override, get_request_with_user,\
    get_request_with_date, fdao_sws_override, fdao_gws_override


@fdao_upass_override
@fdao_sws_override
@fdao_gws_override
class TestUPassDao(TestCase):

    def test_around_qtr_begin(self):
        req = get_request_with_date("2012-12-31 00:00:00")
        self.assertFalse(around_qtr_begin(req))
        req = get_request_with_date("2012-12-31 00:00:01")
        self.assertTrue(around_qtr_begin(req))
        req = get_request_with_date("2013-01-21 23:59:59")
        self.assertTrue(around_qtr_begin(req))
        req = get_request_with_date("2013-01-22 00:00:00")
        self.assertFalse(around_qtr_begin(req))

        req = get_request_with_date("2013-06-17 00:00:00")
        self.assertFalse(around_qtr_begin(req))
        req = get_request_with_date("2013-06-17 00:00:01")
        self.assertTrue(around_qtr_begin(req))
        req = get_request_with_date("2013-07-08 23:59:59")
        self.assertTrue(around_qtr_begin(req))
        req = get_request_with_date("2013-07-09 00:00:00")
        self.assertFalse(around_qtr_begin(req))

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
        req = get_request_with_user("jnew",
                                    get_request_with_date("2013-06-24"))
        status = get_upass(req)
        self.assertFalse(status['is_current'])
        self.assertTrue('in_summer' not in status)
        try:
            self.assertFalse(status['display_activation'])
            self.fail("Non current should not have activation message")
        except KeyError:
            pass

        req = get_request_with_date("2013-04-1")
        req = get_request_with_user("seagrad", req)
        status = get_upass(req)
        self.assertTrue(status['is_current'])
        self.assertTrue(status['display_activation'])
        self.assertFalse(status['in_summer'])

        req = get_request_with_date("2013-09-17")
        req = get_request_with_user("botgrad", req)
        status = get_upass(req)
        self.assertTrue(status['is_current'])
        self.assertTrue(status['in_summer'])
        self.assertFalse(status['display_activation'])

        req = get_request_with_date("2013-10-10")
        req = get_request_with_user("tacgrad", req)
        status = get_upass(req)
        self.assertTrue(status['is_current'])
        self.assertFalse(status['display_activation'])

        req = get_request_with_user("staff")
        status = get_upass(req)
        self.assertFalse(status['is_current'])
        self.assertTrue('display_activation' not in status)

    def test_error(self):
        req = get_request_with_user("jerror")
        self.assertRaises(Exception,
                          get_upass,
                          req)

        req = get_request_with_user("none")
        self.assertRaises(DataFailureException,
                          get_upass,
                          req)
