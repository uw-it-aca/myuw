import logging
from django.http import HttpResponse
from django.utils import simplejson as json
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.finance import get_account_balances_for_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response


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
        return HttpResponse(json.dumps(balances.json_data()))

