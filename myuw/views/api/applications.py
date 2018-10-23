import logging
import traceback
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call, log_data_not_found_response
from restclients_core.exceptions import DataFailureException
from myuw.dao.applications import get_applications
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception, data_not_found

logger = logging.getLogger(__name__)


class Applications(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/applications/.
    """

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the application statuses
        """

        timer = Timer()
        try:
            response = get_applications(request)
            log_api_call(timer, request, "Get Applications")
            return self.json_response(response)
        except Exception as ex:
            if (isinstance(ex, DataFailureException) and ex.status == 404):
                log_data_not_found_response(logger, timer)
                return data_not_found()
            return handle_exception(logger, timer, traceback)
