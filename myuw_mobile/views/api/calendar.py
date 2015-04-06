from django.http import HttpResponse
import json
from myuw_mobile.dao.calendar import api_request
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found


class DepartmentalCalendar(RESTDispatch):
    def GET(self, request):
        response = api_request(request)
        return HttpResponse(json.dumps(response))
