import json
from django.http import HttpResponse
from myuw_mobile.dao.schedule import get_schedule_by_term
from myuw_mobile.dao.term import get_current_quarter
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response
from myuw_mobile.logger.logresp import log_success_response
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.views.api.base_schedule import load_schedule
import logging


class Weekly(RESTDispatch):
    """
    Handles /api/v1/grades/
    """
    def GET(self, request):
        timer = Timer()
        logger = logging.getLogger(__name__)

        term = get_current_quarter(request)
        schedule = get_schedule_by_term(term)
        if schedule is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        if not schedule.json_data():
            log_data_not_found_response(logger, timer)
            return HttpResponse({})

        json_data = {
            "current_week": term.get_week_of_term(),
            "schedule": load_schedule(schedule),
        }
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(json_data),
                            {"Content-Type": "application/json"})
