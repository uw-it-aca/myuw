# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import traceback
import logging
from myuw.dao import is_action_disabled
from myuw.dao.user_pref import set_no_onboard_message, turn_off_pop_up
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception
from myuw.views.exceptions import DisabledAction

logger = logging.getLogger(__name__)


class CloseBannerMsg(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, close the banner message
        """
        timer = Timer()
        try:
            if is_action_disabled():
                raise DisabledAction(
                    "Close Banner Message w. Overriding")

            pref = set_no_onboard_message(request)
            log_api_call(timer, request, "Closed Banner Message")
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
            if is_action_disabled():
                raise DisabledAction(
                    "Turn Off Tour Popup w. Overriding")

            pref = turn_off_pop_up(request)
            log_api_call(timer, request, "Turn Off Tour Popup")
            return self.json_response(
                {'done': pref.display_pop_up is False})
        except Exception:
            return handle_exception(logger, timer, traceback)
