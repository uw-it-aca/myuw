from django.test import TestCase
from django.conf import settings
from myuw_mobile.dao.grad import get_grad_degree_for_current_user,\
    get_grad_committee_for_current_user, get_leave_by_regid,\
    get_grad_petition_for_current_user, json_data_leave
from django.test.client import RequestFactory


FDAO_PWS = 'restclients.dao_implementation.pws.File'
FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_GRA = 'restclients.dao_implementation.grad.File'


class TestGrad(TestCase):

    def test_get_grad_degree_for_current_user(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            degree_reqs = get_grad_degree_for_current_user()
            self.assertIsNotNone(degree_reqs)

    def test_get_grad_committee_for_current_user(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            committee_reqs = get_grad_committee_for_current_user()
            self.assertIsNotNone(committee_reqs)

    def test_get_grad_leave_for_current_user(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            leave_reqs = get_leave_by_regid('9136CCB8F66711D5BE060004AC494FFE')
            self.assertIsNotNone(leave_reqs)
            self.assertEquals(len(leave_reqs), 5)
            now_request = RequestFactory().get("/")
            # winter
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-07"
            json_data = json_data_leave(leave_reqs, now_request)
            self.assertEquals(len(json_data), 4)
            leave = json_data[0]
            self.assertEquals(leave["status"], "requested")
            leave = json_data[1]
            self.assertEquals(leave["status"], "withdrawn")
            leave = json_data[2]
            self.assertEquals(leave["status"], "paid")
            leave = json_data[3]
            self.assertEquals(leave["status"], "approved")
            self.assertEquals(len(leave["terms"]), 1)

            # spring
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-07"
            json_data = json_data_leave(leave_reqs, now_request)
            self.assertEquals(len(json_data), 3)
            leave = json_data[0]
            self.assertEquals(leave["status"], "requested")
            leave = json_data[1]
            self.assertEquals(leave["status"], "withdrawn")
            leave = json_data[2]
            self.assertEquals(leave["status"], "approved")
            self.assertEquals(len(leave["terms"]), 1)

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-06-08"
            json_data = json_data_leave(leave_reqs, now_request)
            self.assertEquals(len(json_data), 2)
            leave = json_data[0]
            self.assertEquals(leave["status"], "requested")
            leave = json_data[1]
            self.assertEquals(leave["status"], "withdrawn")

            # summer
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-08-28"
            json_data = json_data_leave(leave_reqs, now_request)
            self.assertEquals(len(json_data), 1)
            leave = json_data[0]
            self.assertEquals(leave["status"], "requested")

    def test_get_grad_petition_for_current_user(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            petition_reqs = get_grad_petition_for_current_user()
            self.assertIsNotNone(petition_reqs)
