# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.dao.upass import get_upass
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class UPass(ProtectedAPI):
    """
    Performs actions on /api/v1/upass
    """
    def get(self, request, *args, **kwargs):
        timer = Timer()
        try:
            status_json = get_upass(request)
            log_api_call(timer, request, "Get UPass")
            return self.json_response(status_json)
        except Exception:
            return handle_exception(logger, timer, traceback)
