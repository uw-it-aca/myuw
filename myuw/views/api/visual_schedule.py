import logging
import traceback
from myuw.dao.visual_schedule import get_current_visual_schedule, \
    get_schedule_json, get_future_visual_schedule
from myuw.dao.term import get_current_quarter, get_specific_term, is_past, \
    is_in_summer_a_term, is_in_summer_b_term
from myuw.dao.card_display_dates import in_show_grades_period
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg
from myuw.views.error import handle_exception, invalid_future_term, \
    data_not_found
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
            if visual_schedule is None:
                return data_not_found()
            term = get_current_quarter(request)
            summer_term = None
            if term.quarter == "summer":
                if is_in_summer_a_term(request):
                    summer_term = 'a-term'
                elif is_in_summer_b_term(request):
                    summer_term = 'b-term'
            response = get_schedule_json(visual_schedule, term, summer_term)

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
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        summer_term = kwargs.get("summer_term", None)
        timer = Timer()
        try:
            term = get_specific_term(year, quarter)

            if is_past(term, request):
                if not in_show_grades_period(term, request):
                    log_msg(logger, timer, "Future term has passed")
                    return invalid_future_term()
            visual_schedule = get_future_visual_schedule(term, summer_term)
            if visual_schedule is None:
                return data_not_found()
            response = get_schedule_json(visual_schedule, term, summer_term)

            resp = self.json_response(response)
            return resp
        except Exception:
            return handle_exception(logger, timer, traceback)
