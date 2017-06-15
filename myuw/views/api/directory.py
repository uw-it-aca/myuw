import json
import traceback
import logging
from django.http import HttpResponse
from myuw.dao.pws import get_person_of_current_user
from myuw.views.error import handle_exception
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.rest_dispatch import RESTDispatch


logger = logging.getLogger(__name__)


class MyDirectoryInfo(RESTDispatch):

    def GET(self, request):
        """
        GET returns 200 with PWS entry for the current user
        """
        timer = Timer()
        try:
            person = get_person_of_current_user()
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(self._json_directory(person)))
        except Exception:
            return handle_exception(logger, timer, traceback)

    def _json_directory(self, person):
        json = person.json_data()
        json['display_name'] = person.display_name
        return json
