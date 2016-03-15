import logging
import time
import simplejson as json
from django.http import HttpResponse
from myuw.logger.timer import Timer
from myuw.dao.thrive import get_current_message
from myuw.dao.affiliation import is_mandatory_switch_user
from myuw.logger.logresp import log_data_not_found_response,\
    log_success_response
from myuw.views.rest_dispatch import RESTDispatch, data_not_found


class ThriveMessages(RESTDispatch):
    """
    Performs actions on resource at /api/v1/thrive/.
    """

    def GET(self, request):
        """
        GET returns 200 with current thrive message
        for the current user if they are a first year student
        """

        # Hack we're using to identify firstyear students, will need to
        # re-evaluate for AUT 2016
        is_firstyear = is_mandatory_switch_user()

        timer = Timer()
        logger = logging.getLogger(__name__)
        message = None
        if is_firstyear:
            message = get_current_message(request)
        if message is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        return HttpResponse(json.dumps(message))
