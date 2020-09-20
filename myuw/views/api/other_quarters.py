import logging
import traceback
from restclients_core.exceptions import DataFailureException
from myuw.dao.stud_future_terms import get_registered_future_quarters
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class RegisteredFutureQuarters(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/oquarters/.
    """

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the registered future quarters of the current user
                    if not registered, returns 200 with
                                       the future year & quarter.
                    543: data error if SWS having issue
        """
        timer = Timer()
        try:
            try:
                resp_data = get_registered_future_quarters(request)
            except DataFailureException as ex:
                if ex.status != 404:
                    raise
            log_api_call(timer, request, "Get RegisteredFutureQuarters")
            return self.json_response(resp_data)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)
