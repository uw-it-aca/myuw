import traceback
import logging
from myuw.dao import not_overriding
from myuw.dao.user_course_display import set_pin_on_teaching_page
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_msg_with_request
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class CloseMinicard(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, unpins and returns the status of the set pin request
        """
        timer = Timer()
        try:
            if not_overriding():
                section_label = kwargs.get("section_label")
                result = set_pin_on_teaching_page(request, section_label,
                                                  pin=False)
                log_msg_with_request(logger, timer, request,
                                     "CloseMinicard %s" % section_label)
            return self.json_response({"done": result})
        except Exception:
            return handle_exception(logger, timer, traceback)


class PinMinicard(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, pins and returns the status of the set pin request
        """
        timer = Timer()
        try:
            if not_overriding():
                section_label = kwargs.get("section_label")
                result = set_pin_on_teaching_page(request, section_label,
                                                  pin=True)
                log_msg_with_request(logger, timer, request,
                                     "PinMinicard %s" % section_label)
            return self.json_response({"done": result})
        except Exception:
            return handle_exception(logger, timer, traceback)
