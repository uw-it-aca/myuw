import logging
from django.http import HttpResponse
import json
from myuw.views.rest_dispatch import RESTDispatch
from myuw.dao.registered_term import get_registered_future_quarters
from myuw.dao.registered_term import should_highlight_future_quarters
from myuw.dao.term import get_next_non_summer_quarter
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response


class RegisteredFutureQuarters(RESTDispatch):
    """
    Performs actions on resource at /api/v1/oquarters/.
    """

    def GET(self, request):
        """
        GET returns 200 with the registered future quarters
        of the current user
        """

        future_quarters = get_registered_future_quarters(request)
        timer = Timer()
        logger = logging.getLogger(__name__)
        resp_data = {
            "terms": future_quarters
            }

        next_non_summer = get_next_non_summer_quarter(request)
        next_year = next_non_summer.year
        next_quarter = next_non_summer.quarter

        has_registration_for_next_term = False
        for term in future_quarters:
            if (
                    term["quarter"].lower() == next_quarter and
                    term["year"] == next_year and
                    term["section_count"] > 0
                    ):
                has_registration_for_next_term = True

        resp_data["next_term_data"] = {
            "year": next_non_summer.year,
            "quarter": next_non_summer.quarter.capitalize(),
            "has_registration": has_registration_for_next_term,
        }

        highlight = should_highlight_future_quarters(future_quarters, request)
        resp_data["highlight_future_quarters"] = highlight
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))
