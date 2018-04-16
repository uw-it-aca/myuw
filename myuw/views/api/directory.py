import traceback
import logging
from myuw.dao.pws import get_person_of_current_user
from myuw.views.error import handle_exception
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.api import ProtectedAPI

logger = logging.getLogger(__name__)


class MyDirectoryInfo(ProtectedAPI):
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with PWS entry for the current user
        """
        timer = Timer()
        try:
            resp = get_person_of_current_user(request).json_data()
            log_success_response(logger, timer)
            return self.json_response(resp)
        except Exception:
            return handle_exception(logger, timer, traceback)
