import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.uwemail import get_email_forwarding_for_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.rest_dispatch import RESTDispatch, handle_exception


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
        try:
            my_uwemail_forwarding = get_email_forwarding_for_current_user()
            resp_json = my_uwemail_forwarding.json_data()
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(resp_json))
        except Exception:
            return handle_exception(logger, timer, traceback)
