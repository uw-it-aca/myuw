import logging
from django.http import HttpResponse
from myuw.dao.term import get_specific_term, is_past
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_invalid_specified_term, log_msg
from myuw.dao.card_display_dates import in_show_grades_period
from myuw.views.api.base_schedule import StudClasSche
from myuw.views.rest_dispatch import invalid_term, invalid_future_term


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
        """
        timer = Timer()
        smr_term = ""
        if summer_term and len(summer_term) > 1:
            smr_term = summer_term.title()

        request_term = get_specific_term(year, quarter)
        if not request_term:
            log_invalid_specified_term(logger, timer)
            return invalid_term()

        if is_past(request_term, request):
            if not in_show_grades_period(request_term, request):
                log_msg(logger, timer, "Future term has pasted")
                return invalid_future_term()

        return self.make_http_resp(logger, timer, request_term,
                                   request, smr_term)
