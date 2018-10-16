import logging
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.dao.applications import get_applications
from myuw.views.api import ProtectedAPI

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

        response = get_applications(request)

        log_api_call(timer, request, "Get Applications")

        return self.json_response(response)
