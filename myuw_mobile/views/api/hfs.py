import logging
import time
from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.hfs import get_account_balances_for_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response


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
        logger = logging.getLogger(__name__)
        balances = get_account_balances_for_current_user()
        if balances is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        resp_json = balances.json_data(use_custom_date_format=True)
        logger.debug(resp_json)
        return HttpResponse(json.dumps(resp_json))

