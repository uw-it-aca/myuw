# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.dao.idcard_elig import get_idcard_eli
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class IDcardElig(ProtectedAPI):
    """
    Performs actions on /api/v1/idcard-elig
    """
    def get(self, request, *args, **kwargs):
        timer = Timer()
        try:
            status_json = get_idcard_eli(request)
            log_api_call(timer, request, "Get IDcard Eligibility")
            return self.json_response(status_json)
        except Exception:
            return handle_exception(logger, timer, traceback)
