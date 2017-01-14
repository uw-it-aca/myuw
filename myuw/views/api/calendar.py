import json
from django.http import HttpResponse
from myuw.dao.calendar import api_request
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views import prefetch_resources


class DepartmentalCalendar(RESTDispatch):
    def GET(self, request):
        prefetch_resources(request)
        response = api_request(request)
        return HttpResponse(json.dumps(response))
