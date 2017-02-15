import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.library import get_account_info_for_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views.error import handle_exception


logger = logging.getLogger(__name__)


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
        try:
            myaccount = get_account_info_for_current_user()

            resp_json = myaccount.json_data(
                use_abbr_week_month_day_format=True)
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(resp_json))
        except Exception:
            return handle_exception(logger, timer, traceback)
