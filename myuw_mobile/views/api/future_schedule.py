import logging
from django.http import HttpResponse
from myuw_mobile.dao.term import get_quarter, is_past
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

        request_term = get_quarter(year, quarter)
        if not request_term:
            return HttpResponse(status=404)

        if is_past(request_term, request):
            return HttpResponse(status=410)

        return self.make_http_resp(
            logging.getLogger(__name__),
            timer,
            request_term,
            request,
            smr_term)
