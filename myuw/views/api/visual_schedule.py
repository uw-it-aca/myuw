import logging
import traceback
from django.http import HttpResponse
from myuw.dao.visual_schedule import get_current_visual_schedule
from myuw.dao.term import get_current_quarter
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
            response = {}
            visual_schedule = get_current_visual_schedule(request)
            schedule_periods = []
            id = 0
            for period in visual_schedule:
                period_data = period.json_data()
                period_data['id'] = id
                schedule_periods.append(period_data)
                id += 1

            response['periods'] = schedule_periods

            # Add term data for schedule
            term = get_current_quarter(request)
            response['term'] = {
                'year': term.year,
                'quarter': term.quarter
            }
            resp = self.json_response(response)
            return resp
        except Exception:
            return handle_exception(logger, timer, traceback)
