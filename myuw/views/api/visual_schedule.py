import logging
import traceback
from django.http import HttpResponse
from myuw.dao.visual_schedule import get_current_visual_schedule
from myuw.logger.timer import Timer
from myuw.views.error import handle_exception
from myuw.views.api.base_schedule import StudClasSche


logger = logging.getLogger(__name__)


class StuVisSchedCurQtr(StudClasSche):
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
            visual_schedule = get_current_visual_schedule(request)
            return self.json_response(visual_schedule)
        except Exception:
            return handle_exception(logger, timer, traceback)
