import logging
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
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

        response = get_applications()

        log_success_response(logger, timer)

        return self.json_response(response)
