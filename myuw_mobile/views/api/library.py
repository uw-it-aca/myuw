import logging
from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.library import get_account_info_for_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response
from myuw_mobile.logger.logresp import log_success_response


class MyLibInfo(RESTDispatch):
    """
    Performs actions on resource at /api/v1/library/.
    """

    def GET(self, request):
        """
        GET returns 200 with the library account balances
        of the current user
        """

        timer = Timer()
        logger = logging.getLogger(__name__)
        myaccount = get_account_info_for_current_user()
        if myaccount is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        resp_json = myaccount.json_data(use_abbr_week_month_day_format=True)
        logger.debug(resp_json)
        return HttpResponse(json.dumps(resp_json))
