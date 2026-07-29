# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback

from myuw.dao.card_display_dates import in_show_grades_period
from myuw.dao.term import get_specific_term, is_past
from myuw.dao.visual_schedule import (
    get_current_visual_schedule,
    get_future_visual_schedule,
    get_schedule_json,
)
from myuw.logger.logresp import log_api_call
from myuw.logger.timer import Timer
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, handle_exception, invalid_future_term

logger = logging.getLogger(__name__)


class VisSchedCurQtr(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/visual_schedule/current/.
    """

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the current quarter visual schedule
        @return visual schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        try:
            visual_schedule, term, summer_term = (
                get_current_visual_schedule(request))
            if visual_schedule is None:
                return data_not_found()
            response = get_schedule_json(visual_schedule, term, summer_term)
            resp = self.json_response(response)
            log_api_call(timer, request, "Get Current Quarter Visual Schedule")
            return resp
        except Exception:
            return handle_exception(logger, timer, traceback)


class VisSchedOthrQtr(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/visual_schedule/<year>,<quarter>.
    """

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the current quarter visual schedule
        @return visual schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        summer_term = kwargs.get("summer_term", None)
        try:
            term = get_specific_term(year, quarter)

            if is_past(term, request) and not in_show_grades_period(term, request):
                return invalid_future_term(f"{year},{quarter}")

            visual_schedule = get_future_visual_schedule(request, term,
                                                         summer_term)
            if visual_schedule is None:
                return data_not_found()
            response = get_schedule_json(visual_schedule, term, summer_term)

            resp = self.json_response(response)
            log_api_call(timer, request, f"Get Visual Schedule for {year},{quarter}")
            return resp
        except Exception:
            return handle_exception(logger, timer, traceback)
