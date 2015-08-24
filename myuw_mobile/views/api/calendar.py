from django.http import HttpResponse
import json
from myuw.dao.calendar import api_request
from myuw.views.rest_dispatch import RESTDispatch, data_not_found


class DepartmentalCalendar(RESTDispatch):
    def GET(self, request):
        response = api_request(request)
        return HttpResponse(json.dumps(response))
