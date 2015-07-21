from django.test import TestCase
from django.conf import settings
from myuw_mobile.dao.grad import get_grad_degree_for_current_user,\
    get_grad_committee_for_current_user, get_grad_leave_for_current_user,\
    get_grad_petition_for_current_user, get_json
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
            self.assertIsNone(degree_reqs)

    def test_get_grad_committee_for_current_user(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            committee_reqs = get_grad_committee_for_current_user()
            self.assertIsNone(committee_reqs)

    def test_get_grad_leave_for_current_user(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            leave_reqs = get_grad_leave_for_current_user()
            self.assertIsNone(leave_reqs)

    def test_get_grad_petition_for_current_user(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_GRAD_DAO_CLASS=FDAO_GRA):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            petition_reqs = get_grad_petition_for_current_user()
            self.assertIsNone(petition_reqs)
