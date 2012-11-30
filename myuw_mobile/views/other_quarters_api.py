from django.http import HttpResponse
from django.utils import simplejson as json
import logging
from rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.sws import Quarter, Schedule
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response

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
        
        resp_data = { "not_registered": True, 
                      "terms": []
                      }
        terms = []
        term = Quarter()
        sche = Schedule()
        next_quarter_sche = sche.get_next_quarter_schedule()
        if next_quarter_sche is not None and len(next_quarter_sche.sections) > 0:
            terms.append(term.get_next_quarter().json_data())
            resp_data["not_registered"] = False

        if term.is_cur_quar_spring():
            next_fall_quarter_sche = sche.get_next_fall_quarter_schedule() 
            if next_fall_quarter_sche is not None and len(next_fall_quarter_sche.sections) > 0:
                terms.append(term.get_next_fall_quarter().json_data())
                resp_data["not_registered"] = False

        resp_data["terms"] = terms

        #print resp_data
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))

