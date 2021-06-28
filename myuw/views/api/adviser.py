# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import time
import traceback
from myuw.dao.adviser import get_academic_advisers
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class Advisers(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/advisers/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the academic advisers
        of the current user
        """
        timer = Timer()
        try:
            advisers = get_academic_advisers(request)
            resp_json = []
            for advs in advisers:
                resp_json.append(advs.json_data())

            log_api_call(timer, request, "Get Advisers")
            return self.json_response(resp_json)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)
