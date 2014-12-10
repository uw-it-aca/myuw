import logging
from django.http import HttpResponse
from myuw_mobile.dao.term import get_quarter
from myuw_mobile.logger.timer import Timer
from myuw_mobile.views.api.base_schedule import StudClasSche


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

        return self.make_http_resp(
            logging.getLogger(__name__),
            timer,
            get_quarter(year, quarter),
            request,
            smr_term)
