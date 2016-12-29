from django.http import HttpResponse
import json
from myuw.dao.pws import person_prefetch
from myuw.dao.affiliation import affiliation_prefetch
from myuw.dao.term import current_terms_prefetch
from myuw.dao.calendar import api_request
from myuw.views.rest_dispatch import RESTDispatch, data_not_found
from myuw.views import prefetch


class DepartmentalCalendar(RESTDispatch):
    def GET(self, request):
        prefetch_calendar_resources(request)
        response = api_request(request)
        return HttpResponse(json.dumps(response))


def prefetch_calendar_resources(request):
    prefetch_methods = []
    prefetch_methods.extend(affiliation_prefetch())
    prefetch_methods.extend(current_terms_prefetch(request))
    prefetch_methods.extend(person_prefetch())
    prefetch(request, prefetch_methods)
