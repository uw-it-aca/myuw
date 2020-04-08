import logging
import traceback
from restclients_core.exceptions import DataFailureException
from myuw.dao.gws import is_grad_student
from myuw.dao.grad import (
    get_grad_degree_for_current_user, get_grad_committee_for_current_user,
    get_grad_leave_for_current_user, get_grad_petition_for_current_user,
    degree_to_json, committee_to_json, leave_to_json, petition_to_json)
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg, log_api_call, log_exception
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, handle_exception

logger = logging.getLogger(__name__)


class MyGrad(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/grad/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the student account balances
        of the current user
        """
        timer = Timer()
        try:
            if not is_grad_student(request):
                log_msg(logger, timer, "Not a grad student, abort!")
                return data_not_found()

            json_ret = {"degrees": None,
                        "committees": None,
                        "leaves": None,
                        "petitions": None}

            try:
                committee_reqs = get_grad_committee_for_current_user(request)
                json_ret["committees"] = committee_to_json(committee_reqs)
            except DataFailureException as ex:
                if ex.status != 404:
                    json_ret["comm_err"] = ex.status
                    log_exception(logger, "get_grad_committee", traceback)

            try:
                degree_reqs = get_grad_degree_for_current_user(request)
                json_ret["degrees"] = degree_to_json(degree_reqs, request)
            except DataFailureException as ex:
                if ex.status != 404:
                    json_ret["degree_err"] = ex.status
                    log_exception(logger, "get_grad_degree", traceback)

            try:
                leave_reqs = get_grad_leave_for_current_user(request)
                json_ret["leaves"] = leave_to_json(leave_reqs, request)
            except DataFailureException as ex:
                if ex.status != 404:
                    json_ret["leave_err"] = ex.status
                    log_exception(logger, "get_grad_leave", traceback)

            try:
                petition_reqs = get_grad_petition_for_current_user(request)
                json_ret["petitions"] = petition_to_json(
                    petition_reqs, request)
            except DataFailureException as ex:
                if ex.status != 404:
                    json_ret["petit_err"] = ex.status
                    log_exception(logger, "get_grad_leave", traceback)

            log_api_call(timer, request, "Get My Grad")

            return self.json_response(json_ret)
        except Exception:
            return handle_exception(logger, timer, traceback)
