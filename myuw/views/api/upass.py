import logging
import traceback
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.dao.upass import get_upass
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class UPass(ProtectedAPI):
    """
    Performs actions on /api/v1/upass
    """
    def get(self, request, *args, **kwargs):
        timer = Timer()
        try:
            status_json = get_upass(request)
            log_success_response(logger, timer)
            return self.json_response(status_json)
        except Exception:
            return handle_exception(logger, timer, traceback)
