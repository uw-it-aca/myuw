import logging
import traceback
from django.http import HttpResponse
from myuw.dao.term import get_current_quarter
from myuw.logger.timer import Timer
from myuw.views.error import handle_exception
from myuw.views.api.base_schedule import StudClasSche


logger = logging.getLogger(__name__)


class StudClasScheCurQuar(StudClasSche):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """

    def GET(self, request):
        """
        GET returns 200 with the current quarter course section schedule
        @return class schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        try:
            return self.make_http_resp(timer,
                                       get_current_quarter(request),
                                       request)
        except Exception:
            return handle_exception(logger, timer, traceback)
