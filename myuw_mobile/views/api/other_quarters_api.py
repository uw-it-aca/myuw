from django.http import HttpResponse
from django.utils import simplejson as json
import logging
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.sws import Schedule
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_success_response

class RegisteredFutureQuarters(RESTDispatch):
    """
    Performs actions on resource at /api/v1/oquarters/.
    """

    def GET(self, request):
        """ 
        GET returns 200 with the registered future quarters 
        of the current user
        """

        timer = Timer()
        logger = logging.getLogger('myuw_mobile.views.other_quarters_api.RegisteredFutureQuarters.GET')
        
        resp_data = { 
                      "terms": Schedule().get_registered_future_quarters()
                      }
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))

