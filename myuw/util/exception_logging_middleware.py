import logging
import traceback
from myuw.views.error import data_error
from myuw.logger.logback import log_exception

logger = logging.getLogger(__name__)


class ExceptionLogMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return request

    def process_exception(self, request, exception):
        action_string = "Error loading: %s" % request.get_full_path()
        log_exception(logger, action_string, traceback.format_exc())
        return data_error()
