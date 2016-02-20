import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.gws import is_grad_student
from myuw.dao.grad import get_grad_degree_for_current_user,\
    get_grad_committee_for_current_user, get_grad_leave_for_current_user,\
    get_grad_petition_for_current_user, get_json
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg, log_success_response, log_err
from myuw.views.rest_dispatch import RESTDispatch, data_error, data_not_found


logger = logging.getLogger(__name__)


class MyGrad(RESTDispatch):
    """
    Performs actions on resource at /api/v1/grad/.
    """

    def GET(self, request):
        """
        GET returns 200 with the student account balances
        of the current user
        """
        timer = Timer()
        try:
            if not is_grad_student():
                log_msg(logger, timer, "Not a grad student, abort!")
                return data_not_found()

            degree_reqs = get_grad_degree_for_current_user()
            committee_reqs = get_grad_committee_for_current_user()
            leave_reqs = get_grad_leave_for_current_user()
            petition_reqs = get_grad_petition_for_current_user()

            grad_json_data = get_json(degree_reqs, committee_reqs,
                                      leave_reqs, petition_reqs,
                                      request)

            log_success_response(logger, timer)
            return HttpResponse(json.dumps(grad_json_data))
        except Exception:
            log_err(logger, timer, traceback.format_exc())
            return data_error()
