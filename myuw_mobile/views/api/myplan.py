from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found
from restclients.myplan import get_plan
from myuw_mobile.dao.pws import get_regid_of_current_user
from myuw_mobile.dao.term import get_current_quarter


class MyPlan(RESTDispatch):
    """
    Performs actions on /api/v1/myplan
    """

    def GET(self, request):
        quarter = get_current_quarter(request)
        plan = get_plan(regid=get_regid_of_current_user(),
                        year=quarter.year,
                        quarter=quarter.quarter,
                        terms=4)

        return HttpResponse(json.dumps(plan.json_data()))
