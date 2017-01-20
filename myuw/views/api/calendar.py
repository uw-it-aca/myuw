import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.calendar import api_request
from myuw.views.rest_dispatch import RESTDispatch, handle_exception
from myuw.views import prefetch_resources
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response


logger = logging.getLogger(__name__)

class DepartmentalCalendar(RESTDispatch):
    def GET(self, request):
        timer = Timer()
        try:
            prefetch_resources(request,
                               prefetch_person=True)
            response = api_request(request)
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(response))
        except Exception:
            return handle_exception(logger, timer, traceback)
