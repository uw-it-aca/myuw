import traceback
import logging
from myuw.dao.user_pref import set_no_onboard_message, turn_off_pop_up
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg_with_affiliation
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
            pref = set_no_onboard_message(request)
            log_msg_with_affiliation(logger, timer, request,
                                     "Closed Banner Message")
            return self.json_response(
                {'done': pref.display_onboard_message is False})
        except Exception:
            return handle_exception(logger, timer, traceback)


class TurnOffPopup(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, close the banner message
        """
        timer = Timer()
        try:
            pref = turn_off_pop_up(request)
            log_msg_with_affiliation(logger, timer, request,
                                     "Turned Off Tour Popup")
            return self.json_response(
                {'done': pref.display_pop_up is False})
        except Exception:
            return handle_exception(logger, timer, traceback)
