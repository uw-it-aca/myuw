# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from restclients_core.exceptions import DataFailureException
from myuw.dao.myplan import get_plan
from myuw.dao.card_display_dates import during_myplan_peak_load
from myuw.dao.term import get_comparison_datetime
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call, log_msg
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class MyPlan(ProtectedAPI):
    """
    Performs actions on /api/v1/myplan
    """
    def get(self, request, *args, **kwargs):
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        timer = Timer()
        try:
            no_myplan_access = during_myplan_peak_load(
                get_comparison_datetime(request), request)
            if no_myplan_access:
                log_msg(logger, timer,
                        "No MyPlan access during their peak load, abort!")
                return self.json_response([])

            plan_json = get_plan(request, year, quarter)
            log_api_call(timer, request, "Get MyPlan")
            return self.json_response(plan_json)
        except Exception as ex:
            if (isinstance(ex, DataFailureException) and
                    ex.status == 404):
                return self.json_response([])
            return handle_exception(logger, timer, traceback)
