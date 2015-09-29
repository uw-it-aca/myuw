import logging
from django.http import HttpResponse
import json
from myuw.views.rest_dispatch import RESTDispatch, data_not_found
from myuw.dao.finance import get_account_balances_for_current_user
from myuw.dao.notice import get_tuition_due_date
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_data_not_found_response
from myuw.logger.logresp import log_success_response


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
        logger = logging.getLogger(__name__)
        balances = get_account_balances_for_current_user()

        if balances is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        logger.debug(balances.json_data())
        date = get_tuition_due_date()
        response = balances.json_data()
        response['tuition_due'] = str(date)

        return HttpResponse(json.dumps(response))
