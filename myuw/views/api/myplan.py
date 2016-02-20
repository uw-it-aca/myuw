import json
import logging
import traceback
from django.http import HttpResponse
from restclients.myplan import get_plan
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_current_quarter
from myuw.views.rest_dispatch import RESTDispatch
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_err


logger = logging.getLogger(__name__)


class MyPlan(RESTDispatch):
    """
    Performs actions on /api/v1/myplan
    """

    def GET(self, request):
        timer = Timer()
        try:
            quarter = get_current_quarter(request)
            plan = get_plan(regid=get_regid_of_current_user(),
                            year=quarter.year,
                            quarter=quarter.quarter,
                            terms=4)
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(plan.json_data()))
        except Exception:
            # Log the error, but don't have the front end complain
            log_err(logger, timer, traceback.format_exc())
            return HttpResponse('[]')
