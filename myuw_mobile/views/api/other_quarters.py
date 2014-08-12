import logging
from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.registered_term import get_registered_future_quarters
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

        timer = Timer()
        logger = logging.getLogger(__name__)
        resp_data = {
            "terms": get_registered_future_quarters()
            }
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))

