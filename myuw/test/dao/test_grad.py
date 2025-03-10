# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import date, datetime, timedelta
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from myuw.dao.grad import (
    get_grad_degree_for_current_user, committee_to_json,
    get_grad_committee_for_current_user, get_grad_leave_for_current_user,
    get_grad_petition_for_current_user, leave_to_json, petition_to_json,
    is_before_eof_2weeks_since_decision_date, degree_to_json)
from myuw.test import get_request_with_date, get_request_with_user
from uw_grad.util import fdao_grad_override


@fdao_grad_override
class TestDaoGrad(TestCase):

    def test_get_grad_committee(self):
        req = get_request_with_user("seagrad")
        committee_reqs = get_grad_committee_for_current_user(req)
        self.assertIsNotNone(committee_reqs)
        self.assertEqual(len(committee_reqs), 3)

        json_data = committee_to_json(committee_reqs)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 3)
        self.assertEqual(len(json_data[1]['members']), 3)
        self.assertEqual(len(json_data[2]['members']), 4)

        req = get_request_with_user("botgrad")
        committee_reqs = get_grad_committee_for_current_user(req)
        self.assertEqual(len(committee_reqs), 0)
        self.assertIsNone(committee_to_json(committee_reqs))

    def test_get_grad_degree(self):
        req = get_request_with_user("tacgrad")
        degree_reqs = get_grad_degree_for_current_user(req)
        self.assertIsNotNone(degree_reqs)
        self.assertEqual(len(degree_reqs), 0)
        self.assertIsNone(degree_to_json(degree_reqs, req))

        req = get_request_with_user("seagrad")
        degree_reqs = get_grad_degree_for_current_user(req)
        self.assertIsNotNone(degree_reqs)
        self.assertEqual(len(degree_reqs), 8)

        now_request = get_request_with_date("2013-04-24")
        json_data = degree_to_json(degree_reqs, now_request)
        self.assertEqual(len(json_data), 8)
        degree = json_data[4]
        self.assertEqual(degree["status"], "Withdrawn")

        now_request = get_request_with_date("2013-04-25")
        json_data = degree_to_json(degree_reqs, now_request)
        self.assertEqual(len(json_data), 7)
        degree = json_data[4]
        self.assertEqual(degree["status"], "Candidacy Granted")

        now_request = get_request_with_date("2013-08-27")
        json_data = degree_to_json(degree_reqs, now_request)
        self.assertEqual(len(json_data), 7)
        degree = json_data[0]
        self.assertTrue(degree["status"].startswith("Awaiting "))
        degree = json_data[1]
        self.assertTrue(degree["status"].startswith("Awaiting "))
        degree = json_data[2]
        self.assertTrue(degree["status"].startswith("Awaiting "))
        degree = json_data[3]
        self.assertEqual(degree["status"], "Recommended by Dept")
        degree = json_data[4]
        self.assertEqual(degree["status"], "Candidacy Granted")
        degree = json_data[5]
        self.assertEqual(degree["status"], "Graduated by Grad School")
        degree = json_data[6]
        self.assertEqual(degree["status"], "Did Not Graduate")

        # after the end of following term
        now_request = get_request_with_date("2013-08-28")
        json_data = degree_to_json(degree_reqs, now_request)
        self.assertEqual(len(json_data), 4)
        degree = json_data[0]
        self.assertTrue(degree["status"].startswith("Awaiting "))
        degree = json_data[1]
        self.assertTrue(degree["status"].startswith("Awaiting "))
        degree = json_data[2]
        self.assertTrue(degree["status"].startswith("Awaiting "))
        degree = json_data[3]
        self.assertEqual(degree["status"], "Recommended by Dept")

    def test_is_before_eof_2weeks_since_decision_date(self):
        self.assertTrue(is_before_eof_2weeks_since_decision_date(
                datetime(2013, 2, 10, 0, 0, 0),
                datetime(2013, 2, 24, 0, 0, 0)))
        self.assertFalse(is_before_eof_2weeks_since_decision_date(
                datetime(2013, 2, 10, 0, 0, 0),
                datetime(2013, 2, 25, 0, 0, 0)))
        self.assertTrue(is_before_eof_2weeks_since_decision_date(
                datetime(2013, 6, 10, 0, 0, 0),
                datetime(2013, 6, 10, 0, 0, 0)))
        self.assertTrue(is_before_eof_2weeks_since_decision_date(
                None,
                datetime(2013, 6, 10, 0, 0, 0)))

    def test_get_grad_leave(self):
        req = get_request_with_user("botgrad")
        leave_reqs = get_grad_leave_for_current_user(req)
        self.assertIsNotNone(leave_reqs)
        self.assertEqual(len(leave_reqs), 0)
        self.assertIsNone(leave_to_json(leave_reqs, req))

        req = get_request_with_user("seagrad")
        leave_reqs = get_grad_leave_for_current_user(req)
        self.assertIsNotNone(leave_reqs)
        self.assertEqual(len(leave_reqs), 5)

        now_request = get_request_with_date("2012-12-07")
        json_data = leave_to_json(leave_reqs, now_request)
        self.assertEqual(len(json_data), 5)
        leave = json_data[2]
        self.assertEqual(leave["status"], "Paid")
        leave = json_data[3]
        self.assertEqual(leave["status"], "Denied")
        # denied shows until eof 2012 autumn
        leave = json_data[4]
        self.assertEqual(leave["status"], "Approved")
        # the 1st approved shows until eof last instruction 2012 autumn
        # the 2nd approved shows until eof last instruction 2013 spring
        self.assertEqual(len(leave["terms"]), 2)

        now_request = get_request_with_date("2012-12-08")
        json_data = leave_to_json(leave_reqs, now_request)
        self.assertEqual(len(json_data), 5)
        leave = json_data[2]
        self.assertEqual(leave["status"], "Paid")
        # paid shows until eof 2013 winter
        leave = json_data[4]
        self.assertEqual(leave["status"], "Approved")
        self.assertEqual(len(leave["terms"]), 2)

        now_request = get_request_with_date("2013-01-07")
        json_data = leave_to_json(leave_reqs, now_request)
        self.assertEqual(len(json_data), 4)
        leave = json_data[2]
        self.assertEqual(leave["status"], "Paid")
        # paid shows until eof 2013 winter
        leave = json_data[3]
        self.assertEqual(leave["status"], "Approved")
        # the end of winter 2013
        now_request = get_request_with_date("2013-03-27")
        json_data = leave_to_json(leave_reqs, now_request)
        self.assertEqual(len(json_data), 3)
        leave = json_data[0]
        self.assertEqual(leave["status"], "Requested")
        leave = json_data[1]
        self.assertEqual(leave["status"], "Withdrawn")
        leave = json_data[2]
        self.assertEqual(leave["status"], "Approved")
        self.assertEqual(len(leave["terms"]), 1)
        # this approved shows until eof last instruction 2013 spring
        now_request = get_request_with_date("2013-06-07")
        json_data = leave_to_json(leave_reqs, now_request)
        self.assertEqual(len(json_data), 3)
        leave = json_data[0]
        self.assertEqual(leave["status"], "Requested")
        leave = json_data[1]
        self.assertEqual(leave["status"], "Withdrawn")
        leave = json_data[2]
        self.assertEqual(leave["status"], "Approved")
        self.assertEqual(len(leave["terms"]), 1)
        # this approved shows until eof last instruction 2013 spring
        now_request = get_request_with_date("2013-06-08")
        json_data = leave_to_json(leave_reqs, now_request)
        self.assertEqual(len(json_data), 2)
        leave = json_data[0]
        self.assertEqual(leave["status"], "Requested")
        leave = json_data[1]
        self.assertEqual(leave["status"], "Withdrawn")
        # withdrawn shows until eof 2013 summer
        now_request = get_request_with_date("2013-08-28")
        json_data = leave_to_json(leave_reqs, now_request)
        self.assertEqual(len(json_data), 1)
        leave = json_data[0]
        self.assertEqual(leave["status"], "Requested")
        # requested always shows

        req = get_request_with_user("tacgrad")
        leave_reqs = get_grad_leave_for_current_user(req)
        self.assertIsNotNone(leave_reqs)
        self.assertEqual(len(leave_reqs), 7)
        now_request = get_request_with_date("2014-06-19")
        json_data = leave_to_json(leave_reqs, now_request)
        self.assertIsNone(json_data, 0)

    def test_get_grad_petition(self):
        req = get_request_with_user("botgrad")
        petition_reqs = get_grad_petition_for_current_user(req)
        self.assertEqual(len(petition_reqs), 0)
        self.assertIsNone(petition_to_json(petition_reqs, req))

        req = get_request_with_user("seagrad")
        petition_reqs = get_grad_petition_for_current_user(req)
        self.assertIsNotNone(petition_reqs)
        self.assertEqual(len(petition_reqs), 7)

        now_request = get_request_with_date("2013-04-10")
        json_data = petition_to_json(petition_reqs, now_request)
        self.assertEqual(len(json_data), 7)
        peti = json_data[0]
        self.assertEqual(peti["dept_recommend"], "Pending")
        self.assertEqual(peti["gradschool_decision"], "Pending")
        peti = json_data[1]
        self.assertEqual(peti["decision_date"], "2013-04-10T00:00:00")
        self.assertEqual(peti["dept_recommend"], "Withdraw")
        self.assertEqual(peti["gradschool_decision"], "Withdraw")
        now_request = get_request_with_date("2013-04-25")
        json_data = petition_to_json(petition_reqs, now_request)
        self.assertEqual(len(json_data), 3)
        peti = json_data[0]
        self.assertEqual(peti["dept_recommend"], "Pending")
        self.assertEqual(peti["gradschool_decision"], "Pending")
        peti = json_data[1]
        self.assertIsNone(peti["decision_date"])
        self.assertEqual(peti["dept_recommend"], "Deny")
        self.assertEqual(peti["gradschool_decision"], "Pending")
        peti = json_data[2]
        self.assertIsNone(peti["decision_date"])
        self.assertEqual(peti["dept_recommend"], "Approve")
        self.assertEqual(peti["gradschool_decision"], "Pending")
