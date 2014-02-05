from django.http import HttpResponse
from myuw_mobile.views.rest_dispatch import RESTDispatch
from restclients.sws import SWS
import json

class Weekly(RESTDispatch):
    """
    Handles /api/v1/grades/
    """
    def GET(self, request):
        sws = SWS()
        term = sws.get_current_term()

        current_week = term.get_week_of_term()


        json_data = {
            "current_week": current_week
        }

        return HttpResponse(json.dumps(json_data), { "Content-Type": "application/json" })
