import logging
import traceback
from django.http import HttpResponse
from myuw.dao.term import get_specific_term, is_past
from myuw.dao.card_display_dates import in_show_grades_period
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_err, log_msg
from myuw.views.api.base_schedule import StudClasSche
from myuw.views.rest_dispatch import data_error, invalid_future_term


logger = logging.getLogger(__name__)


class StudClasScheFutureQuar(StudClasSche):
    """
    Performs actions on resource at
    /api/v1/schedule/<year>,<quarter>(,<summer_term>)?
    """
    def GET(self, request, year, quarter, summer_term=None):
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
        try:
            smr_term = ""
            if summer_term and len(summer_term) > 1:
                smr_term = summer_term.title()

            request_term = get_specific_term(year, quarter)

            if is_past(request_term, request):
                if not in_show_grades_period(request_term, request):
                    log_msg(logger, timer, "Future term has pasted")
                    return invalid_future_term()

            return self.make_http_resp(timer, request_term,
                                       request, smr_term)
        except Exception:
            log_err(logger, timer, traceback.format_exc())
            return data_error()
