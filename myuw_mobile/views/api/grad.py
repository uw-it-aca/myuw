import logging
from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.grad import get_grad_degree_for_current_user,\
    get_grad_committee_for_current_user, get_grad_leave_for_current_user,\
    get_grad_petition_for_current_user, get_json
# from myuw_mobile.dao.notice import get_grad_notices
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response
from myuw_mobile.logger.logresp import log_success_response


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
        logger = logging.getLogger(__name__)
        degree_reqs = get_grad_degree_for_current_user()
        committee_reqs = get_grad_committee_for_current_user()
        leave_reqs = get_grad_leave_for_current_user()
        petition_reqs = get_grad_petition_for_current_user()

        if degree_reqs is None and committee_reqs is None and\
                leave_reqs is None and petition_reqs is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        grad_json_data = get_json(degree_reqs, committee_reqs,
                                  leave_reqs, petition_reqs)
        logger.debug(grad_json_data)

        return HttpResponse(json.dumps(grad_json_data))
