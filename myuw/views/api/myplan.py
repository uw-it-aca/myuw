from django.http import HttpResponse
import json
from myuw.views.rest_dispatch import RESTDispatch, data_not_found
from restclients.myplan import get_plan
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_current_quarter
import logging

logger = logging.getLogger(__name__)


class MyPlan(RESTDispatch):
    """
    Performs actions on /api/v1/myplan
    """

    def GET(self, request):
        try:
            quarter = get_current_quarter(request)
            plan = get_plan(regid=get_regid_of_current_user(),
                            year=quarter.year,
                            quarter=quarter.quarter,
                            terms=4)

            return HttpResponse(json.dumps(plan.json_data()))
        except Exception as ex:
            # Log the error, but don't have the front end complain
            print ex
            logger.error(ex)
            return HttpResponse('[]')
