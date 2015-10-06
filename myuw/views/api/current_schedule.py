import logging
from django.http import HttpResponse
from myuw.dao.term import get_current_quarter
from myuw.logger.timer import Timer
from myuw.views.api.base_schedule import StudClasSche


class StudClasScheCurQuar(StudClasSche):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """

    def GET(self, request):
        """
        GET returns 200 with the current quarter course section schedule
        """
        return self.make_http_resp(
            logging.getLogger(__name__),
            Timer(),
            get_current_quarter(request),
            request
            )
