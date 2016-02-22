import logging
import time
import simplejson as json
import traceback
from django.http import HttpResponse
from myuw.dao.hfs import get_account_balances_for_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg, log_success_response, log_err
from myuw.views.rest_dispatch import RESTDispatch, data_not_found, data_error


logger = logging.getLogger(__name__)


class HfsBalances(RESTDispatch):
    """
    Performs actions on resource at /api/v1/hfs/.
    """

    def GET(self, request):
        """
        GET returns 200 with the HFS account balances
        of the current user
        """
        timer = Timer()
        try:
            balances = get_account_balances_for_current_user()

            resp_json = balances.json_data(use_custom_date_format=True)
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(resp_json))
        except Exception:
            log_err(logger, timer, traceback.format_exc())
            return data_error()
