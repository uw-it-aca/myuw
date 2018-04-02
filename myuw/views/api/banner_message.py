import traceback
import logging
from myuw.dao.user import set_no_onboard_message
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class CloseBannerMsg(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, close the banner message
        """
        timer = Timer()
        try:
            obj = set_no_onboard_message(request)
            log_success_response(logger, timer)
            return self.json_response({'done': (obj is not None)})
        except Exception:
            return handle_exception(logger, timer, traceback)
