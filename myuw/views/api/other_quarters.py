# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from restclients_core.exceptions import DataFailureException
from myuw.dao.stud_future_terms import get_registered_future_quarters
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class RegisteredFutureQuarters(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/oquarters/.
    """

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the registered future quarters of the current user
                    if not registered, returns 200 with
                                       the future year & quarter.
                    543: data error if SWS having issue
        """
        timer = Timer()
        try:
            data = get_registered_future_quarters(request)
            log_api_call(timer, request, "Get RegisteredFutureQuarters")
            return self.json_response(data)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)
