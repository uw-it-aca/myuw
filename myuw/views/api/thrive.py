# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from myuw.logger.timer import Timer
from myuw.dao.thrive import get_current_message, get_previous_messages
from myuw.logger.logresp import log_data_not_found_response, log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found

logger = logging.getLogger(__name__)


class ThriveMessages(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/thrive/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with current thrive message
        for the current user if they are a first year student
        """
        timer = Timer()
        message = None
        if request.GET.get('history', False):
            message = get_previous_messages(request)
        else:
            message = get_current_message(request)

        if message is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_api_call(timer, request, "Get ThriveMessages")
        return self.json_response(message)
