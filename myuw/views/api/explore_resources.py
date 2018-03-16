import logging
import traceback
from myuw.logger.timer import Timer
from myuw.logger.logresp import (
    log_data_not_found_response, log_msg, log_success_response)
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, handle_exception

logger = logging.getLogger(__name__)


class Explore(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/explore_resources/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the student account balances
        of the current user
        """
        timer = Timer()
        try:
            response = []
            log_success_response(logger, timer)
            return self.json_response(response)
        except Exception:
            return handle_exception(logger, timer, traceback)
