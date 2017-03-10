import json
import logging
import traceback
from django.http import HttpResponse
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views.error import handle_exception
from myuw.dao.upass import get_upass_by_current_user


logger = logging.getLogger(__name__)


class UPass(RESTDispatch):
    """
    Performs actions on /api/v1/upass
    """

    def GET(self, request):
        timer = Timer()
        try:
            status = get_upass_by_current_user()

            log_success_response(logger, timer)
            return HttpResponse(json.dumps({"message": status.status_message}))
        except Exception:
            return handle_exception(logger, timer, traceback)
