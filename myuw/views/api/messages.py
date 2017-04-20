import logging
import simplejson as json
import traceback
from django.http import HttpResponse
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views.error import handle_exception
from myuw.dao.messages import get_current_messages


logger = logging.getLogger(__name__)


class Messages(RESTDispatch):
    """
    Performs actions on resource at /api/v1/messages/.
    """

    def GET(self, request):
        """
        GET returns 200 with the banner messages for the current user
        """
        timer = Timer()
        try:
            messages = get_current_messages(request)
            message_json = []
            for message in messages:
                message_json.append(message.json_data())
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(message_json))
        except Exception as ex:
            return handle_exception(logger, timer, traceback)
