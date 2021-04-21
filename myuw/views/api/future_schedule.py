# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from myuw.dao.term import get_specific_term, is_past
from myuw.dao.card_display_dates import in_show_grades_period
from myuw.logger.timer import Timer
from myuw.views.api.base_schedule import StudClasSche
from myuw.views.error import invalid_future_term, handle_exception

logger = logging.getLogger(__name__)


class StudClasScheFutureQuar(StudClasSche):
    """
    Performs actions on resource at
    /api/v1/schedule/<year>,<quarter>(,<summer_term>)?
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with course section schedule details of
        the given year, quarter.
        Return the course sections of full term and matched term
        if a specific summer-term is given
        @return class schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        summer_term = kwargs.get("summer_term", "full-term")
        try:
            request_term = get_specific_term(year, quarter)
            if is_past(request_term, request):
                if not in_show_grades_period(request_term, request):
                    return invalid_future_term("{},{}".format(year, quarter))

            return self.make_http_resp(
                timer, request_term, request, summer_term=summer_term)
        except Exception:
            return handle_exception(logger, timer, traceback)
