from django.test import TestCase
from django.conf import settings
from datetime import date, datetime, timedelta
from myuw.dao.grad import get_degree_by_regid,\
    get_leave_by_regid, get_committee_by_regid, to_json,\
    get_petition_by_regid, leave_to_json, petition_to_json,\
    is_before_eof_2weeks_since_decision_date, degree_to_json
from django.test.client import RequestFactory


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_GRA = 'restclients.dao_implementation.grad.File'


class TestGrad(TestCase):

    def test_null_system_key(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):
            reqs = get_degree_by_regid('00000000000000000000000000000001')
            self.assertIsNone(reqs)

            reqs = get_committee_by_regid('00000000000000000000000000000001')
            self.assertIsNone(reqs)

            reqs = get_leave_by_regid('00000000000000000000000000000001')
            self.assertIsNone(reqs)

            reqs = get_petition_by_regid('00000000000000000000000000000001')
            self.assertIsNone(reqs)

    def test_get_grad_committee(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            committee_reqs = get_committee_by_regid(
                '9136CCB8F66711D5BE060004AC494FFE')
            self.assertIsNotNone(committee_reqs)
            self.assertEquals(len(committee_reqs), 3)

            committee_reqs = get_committee_by_regid(
                '9136CCB8F66711D5BE060004AC494F31')
            self.assertEquals(len(committee_reqs), 0)
            self.assertIsNone(to_json(committee_reqs))

    def test_get_grad_degree(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")

            degree_reqs = get_degree_by_regid(
                '12345678901234567890123456789012')
            self.assertIsNotNone(degree_reqs)
            self.assertEquals(len(degree_reqs), 0)
            self.assertIsNone(degree_to_json(degree_reqs, now_request))

            degree_reqs = get_degree_by_regid(
                '9136CCB8F66711D5BE060004AC494FFE')
            self.assertIsNotNone(degree_reqs)
            self.assertEquals(len(degree_reqs), 8)

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-24"
            json_data = degree_to_json(degree_reqs, now_request)
            self.assertEquals(len(json_data), 8)
            degree = json_data[4]
            self.assertEquals(degree["status"], "Withdrawn")

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-25"
            json_data = degree_to_json(degree_reqs, now_request)
            self.assertEquals(len(json_data), 7)
            degree = json_data[4]
            self.assertEquals(degree["status"], "Candidacy Granted")

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-27"
            json_data = degree_to_json(degree_reqs, now_request)
            self.assertEquals(len(json_data), 7)
            degree = json_data[0]
            self.assertTrue(degree["status"].startswith("Awaiting "))
            degree = json_data[1]
            self.assertTrue(degree["status"].startswith("Awaiting "))
            degree = json_data[2]
            self.assertTrue(degree["status"].startswith("Awaiting "))
            degree = json_data[3]
            self.assertEquals(degree["status"], "Recommended by Dept")
            degree = json_data[4]
            self.assertEquals(degree["status"], "Candidacy Granted")
            degree = json_data[5]
            self.assertEquals(degree["status"], "Graduated by Grad School")
            degree = json_data[6]
            self.assertEquals(degree["status"], "Did Not Graduate")

            # after the end of following term
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-28"
            json_data = degree_to_json(degree_reqs, now_request)
            self.assertEquals(len(json_data), 4)
            degree = json_data[0]
            self.assertTrue(degree["status"].startswith("Awaiting "))
            degree = json_data[1]
            self.assertTrue(degree["status"].startswith("Awaiting "))
            degree = json_data[2]
            self.assertTrue(degree["status"].startswith("Awaiting "))
            degree = json_data[3]
            self.assertEquals(degree["status"], "Recommended by Dept")

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
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")
            leave_reqs = get_leave_by_regid('9136CCB8F66711D5BE060004AC494F31')
            self.assertIsNotNone(leave_reqs)
            self.assertEquals(len(leave_reqs), 0)
            self.assertIsNone(leave_to_json(leave_reqs, now_request))

            leave_reqs = get_leave_by_regid('9136CCB8F66711D5BE060004AC494FFE')
            self.assertIsNotNone(leave_reqs)
            self.assertEquals(len(leave_reqs), 5)
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-12-07"
            json_data = leave_to_json(leave_reqs, now_request)
            self.assertEquals(len(json_data), 5)
            leave = json_data[2]
            self.assertEquals(leave["status"], "paid")
            leave = json_data[3]
            self.assertEquals(leave["status"], "denied")
            # denied shows until eof 2012 autumn
            leave = json_data[4]
            self.assertEquals(leave["status"], "approved")
            # the 1st approved shows until eof last instruction 2012 autumn
            # the 2nd approved shows until eof last instruction 2013 spring
            self.assertEquals(len(leave["terms"]), 2)

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2012-12-08"
            json_data = leave_to_json(leave_reqs, now_request)
            self.assertEquals(len(json_data), 5)
            leave = json_data[2]
            self.assertEquals(leave["status"], "paid")
            # paid shows until eof 2013 winter
            leave = json_data[4]
            self.assertEquals(leave["status"], "approved")
            self.assertEquals(len(leave["terms"]), 1)

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-01-07"
            json_data = leave_to_json(leave_reqs, now_request)
            self.assertEquals(len(json_data), 4)
            leave = json_data[2]
            self.assertEquals(leave["status"], "paid")
            # paid shows until eof 2013 winter
            leave = json_data[3]
            self.assertEquals(leave["status"], "approved")
            # the end of winter 2013
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-27"
            json_data = leave_to_json(leave_reqs, now_request)
            self.assertEquals(len(json_data), 3)
            leave = json_data[0]
            self.assertEquals(leave["status"], "requested")
            leave = json_data[1]
            self.assertEquals(leave["status"], "withdrawn")
            leave = json_data[2]
            self.assertEquals(leave["status"], "approved")
            self.assertEquals(len(leave["terms"]), 1)
            # this approved shows until eof last instruction 2013 spring
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-07"
            json_data = leave_to_json(leave_reqs, now_request)
            self.assertEquals(len(json_data), 3)
            leave = json_data[0]
            self.assertEquals(leave["status"], "requested")
            leave = json_data[1]
            self.assertEquals(leave["status"], "withdrawn")
            leave = json_data[2]
            self.assertEquals(leave["status"], "approved")
            self.assertEquals(len(leave["terms"]), 1)
            # this approved shows until eof last instruction 2013 spring
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-08"
            json_data = leave_to_json(leave_reqs, now_request)
            self.assertEquals(len(json_data), 2)
            leave = json_data[0]
            self.assertEquals(leave["status"], "requested")
            leave = json_data[1]
            self.assertEquals(leave["status"], "withdrawn")
            # withdrawn shows until eof 2013 summer
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-28"
            json_data = leave_to_json(leave_reqs, now_request)
            self.assertEquals(len(json_data), 1)
            leave = json_data[0]
            self.assertEquals(leave["status"], "requested")
            # requested always shows

            leave_reqs = get_leave_by_regid('12345678901234567890123456789012')
            self.assertIsNotNone(leave_reqs)
            self.assertEquals(len(leave_reqs), 7)
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2014-06-19"
            json_data = leave_to_json(leave_reqs, now_request)
            self.assertIsNone(json_data, 0)

    def test_get_grad_petition(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")

            petition_reqs = get_petition_by_regid(
                '9136CCB8F66711D5BE060004AC494F31')
            self.assertEquals(len(petition_reqs), 0)
            self.assertIsNone(petition_to_json(petition_reqs, now_request))

            petition_reqs = get_petition_by_regid(
                '9136CCB8F66711D5BE060004AC494FFE')
            self.assertIsNotNone(petition_reqs)
            self.assertEquals(len(petition_reqs), 7)

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-10"
            json_data = petition_to_json(petition_reqs, now_request)
            self.assertEquals(len(json_data), 7)
            peti = json_data[0]
            self.assertEqual(peti["dept_recommend"], "Pending")
            self.assertEqual(peti["gradschool_decision"], "Pending")
            peti = json_data[1]
            self.assertEquals(peti["decision_date"], "2013-04-10T00:00:00")
            self.assertEqual(peti["dept_recommend"], "Withdraw")
            self.assertEqual(peti["gradschool_decision"], "Withdraw")
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-04-25"
            json_data = petition_to_json(petition_reqs, now_request)
            self.assertEquals(len(json_data), 3)
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
