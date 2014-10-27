import logging
from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.registered_term import get_registered_future_quarters
from myuw_mobile.dao.registered_term import should_highlight_future_quarters
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_success_response


class RegisteredFutureQuarters(RESTDispatch):
    """
    Performs actions on resource at /api/v1/oquarters/.
    """

    def GET(self, request):
        """ 
        GET returns 200 with the registered future quarters 
        of the current user
        """

        future_quarters = get_registered_future_quarters()
        timer = Timer()
        logger = logging.getLogger(__name__)
        resp_data = {
            "terms": future_quarters
            }

        resp_data["highlight_future_quarters"] = should_highlight_future_quarters(future_quarters)
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))

