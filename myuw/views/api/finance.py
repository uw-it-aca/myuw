import logging
from django.http import HttpResponse
import json
from myuw.dao.gws import is_student
from myuw.dao.finance import get_account_balances_for_current_user
from myuw.dao.notice import get_tuition_due_date
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_data_not_found_response, log_msg,\
    log_success_response
from myuw.views.rest_dispatch import RESTDispatch, data_not_found, data_error


logger = logging.getLogger(__name__)


class Finance(RESTDispatch):
    """
    Performs actions on resource at /api/v1/finance/.
    """

    def GET(self, request):
        """
        GET returns 200 with the student account balances
        of the current user
        """
        timer = Timer()
        if not is_student():
            log_msg(logger, timer, "Not a student, abort!")
            return data_not_found()

        balances = get_account_balances_for_current_user()

        if balances is None:
            log_msg(logger, timer, "Account balances data error")
            return data_error()

        date = get_tuition_due_date()
        response = balances.json_data()
        response['tuition_due'] = str(date)
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(response))
