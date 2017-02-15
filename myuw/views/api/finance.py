import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.gws import is_student
from myuw.dao.finance import get_account_balances_for_current_user
from myuw.dao.notice import get_tuition_due_date
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_data_not_found_response, log_msg,\
    log_success_response
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views.error import data_not_found, handle_exception


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
        try:
            if not is_student():
                log_msg(logger, timer, "Not a student, abort!")
                return data_not_found()

            balances = get_account_balances_for_current_user()

            date = get_tuition_due_date()
            response = balances.json_data()
            response['tuition_due'] = str(date)

            log_success_response(logger, timer)
            return HttpResponse(json.dumps(response))
        except Exception:
            return handle_exception(logger, timer, traceback)
