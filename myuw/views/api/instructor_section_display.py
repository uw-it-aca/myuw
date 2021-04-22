# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import traceback
import logging
from myuw.dao import is_action_disabled
from myuw.dao.instructor_mini_course_card import set_pin_on_teaching_page
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception
from myuw.views.exceptions import DisabledAction

logger = logging.getLogger(__name__)


class CloseMinicard(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, unpins and returns the status of the set pin request
        """
        timer = Timer()
        try:
            if is_action_disabled():
                raise DisabledAction("Close Minicard w. Overriding")

            section_label = kwargs.get("section_label")
            result = set_pin_on_teaching_page(request, section_label,
                                              pin=False)
            log_api_call(timer, request,
                         "Close Minicard {}".format(section_label))
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
            if is_action_disabled():
                raise DisabledAction("Pin Minicard w. Overriding")

            section_label = kwargs.get("section_label")
            result = set_pin_on_teaching_page(request, section_label,
                                              pin=True)
            log_api_call(timer, request,
                         "Pin Minicard {}".format(section_label))
            return self.json_response({"done": result})
        except Exception:
            return handle_exception(logger, timer, traceback)
