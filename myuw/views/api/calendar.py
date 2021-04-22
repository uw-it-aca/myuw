# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from myuw.dao.calendar import api_request
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception
from myuw.views import prefetch_resources
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call

logger = logging.getLogger(__name__)


class DepartmentalCalendar(ProtectedAPI):
    def get(self, request, *args, **kwargs):
        timer = Timer()
        try:
            prefetch_resources(request,
                               prefetch_group=True,
                               prefetch_enrollment=True)
            response = api_request(request)
            log_api_call(timer, request, "Get DepartmentalCalendar")
            return self.json_response(response)
        except Exception:
            return handle_exception(logger, timer, traceback)
