from django.http import HttpResponse
import json
import logging
import traceback
from myuw.dao.pws import person_prefetch
from myuw.dao.affiliation import affiliation_prefetch
from myuw.dao.term import current_terms_prefetch
from myuw.dao.calendar import api_request
from myuw.views.rest_dispatch import RESTDispatch, handle_exception
from myuw.views import prefetch
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response


logger = logging.getLogger(__name__)


class DepartmentalCalendar(RESTDispatch):
    def GET(self, request):
        timer = Timer()
        try:
            prefetch_calendar_resources(request)
            response = api_request(request)
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(response))
        except Exception:
            return handle_exception(logger, timer, traceback)


def prefetch_calendar_resources(request):
    prefetch_methods = []
    prefetch_methods.extend(affiliation_prefetch())
    prefetch_methods.extend(current_terms_prefetch(request))
    prefetch_methods.extend(person_prefetch())
    prefetch(request, prefetch_methods)
