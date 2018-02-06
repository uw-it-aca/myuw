import logging
import traceback
from myuw.dao.calendar import api_request
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception
from myuw.views import prefetch_resources
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response

logger = logging.getLogger(__name__)


class DepartmentalCalendar(ProtectedAPI):
    def get(self, request, *args, **kwargs):
        timer = Timer()
        try:
            prefetch_resources(request,
                               prefetch_group=True,
                               prefetch_enrollment=True)
            response = api_request(request)
            log_success_response(logger, timer)
            return self.json_response(response)
        except Exception:
            return handle_exception(logger, timer, traceback)
