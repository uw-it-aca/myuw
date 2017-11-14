import logging
import traceback
from django.http import HttpResponse
from myuw.dao.visual_schedule import get_current_visual_schedule, \
    get_schedule_json, get_future_visual_schedule
from myuw.dao.term import get_current_quarter
from myuw.logger.timer import Timer
from myuw.views.error import handle_exception
from myuw.views.api import ProtectedAPI


logger = logging.getLogger(__name__)


class VisSchedCurQtr(ProtectedAPI):
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
            term = get_current_quarter(request)
            response = get_schedule_json(visual_schedule, term)

            resp = self.json_response(response)
            return resp
        except Exception:
            return handle_exception(logger, timer, traceback)


class VisSchedOthrQtr(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/visual_schedule/<year>,<quarter>.
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
            term = get_current_quarter(request)
            visual_schedule = get_future_visual_schedule(term)
            response = get_schedule_json(visual_schedule, term)

            resp = self.json_response(response)
            return resp
        except Exception:
            return handle_exception(logger, timer, traceback)
