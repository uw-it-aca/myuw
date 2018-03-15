import traceback
import logging
from myuw.dao.user_course_display import set_pin_on_teaching_page
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class CloseMinicard(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, unpins and returns the status of the set pin request
        """
        section_label = kwargs.get("section_label")
        timer = Timer()
        try:
            result = set_pin_on_teaching_page(request, section_label,
                                              pin=False)
            log_success_response(logger, timer)
            return self.json_response({"done": result})
        except Exception:
            return handle_exception(logger, timer, traceback)


class PinMinicard(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, pins and returns the status of the set pin request
        """
        section_label = kwargs.get("section_label")
        timer = Timer()
        try:
            result = set_pin_on_teaching_page(request, section_label,
                                              pin=True)
            log_success_response(logger, timer)
            return self.json_response({"done": result})
        except Exception:
            return handle_exception(logger, timer, traceback)
