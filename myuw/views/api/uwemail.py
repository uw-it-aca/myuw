import logging
from django.http import HttpResponse
import json
from myuw.dao.uwemail import get_email_forwarding_for_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_msg
from myuw.views.rest_dispatch import RESTDispatch, data_not_found, data_error


logger = logging.getLogger(__name__)


class UwEmail(RESTDispatch):
    """
    Performs actions on resource at /api/v1/uwemail/.
    """

    def GET(self, request):
        """
        GET returns 200 with the uwemail forwarding
        of the current user
        """
        timer = Timer()
        my_uwemail_forwarding = get_email_forwarding_for_current_user()
        if my_uwemail_forwarding is None:
            log_msg(logger, timer, "UwEmail data error")
            return data_error()

        resp_json = my_uwemail_forwarding.json_data()
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_json))
