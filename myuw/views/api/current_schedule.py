import logging
from django.http import HttpResponse
from myuw.dao.term import get_current_quarter
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_invalid_current_term
from myuw.views.api.base_schedule import StudClasSche
from myuw.views.rest_dispatch import invalid_term


logger = logging.getLogger(__name__)


class StudClasScheCurQuar(StudClasSche):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """

    def GET(self, request):
        """
        GET returns 200 with the current quarter course section schedule
        """
        timer = Timer()
        term = get_current_quarter(request)
        if term is None:
            log_invalid_current_term(logger, timer)
            return invalid_term()

        return self.make_http_resp(logger, timer, term, request)
