import logging
from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.student_profile import get_profile_of_current_user
from myuw_mobile.dao.enrollment import get_main_campus
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response


class MyProfile(RESTDispatch):
    """
    Performs actions on resource at /api/v1/profile/.
    """

    def GET(self, request):
        """ 
        GET returns 200 with the student account balances 
        of the current user
        """

        timer = Timer()
        logger = logging.getLogger(__name__)
        profile = get_profile_of_current_user()
        if profile is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        logger.debug(profile.json_data())

        response = profile.json_data()
        campuses = get_main_campus()
        if campuses is not None and len(campuses) > 0:
            response['campus'] = campuses[0]
        return HttpResponse(json.dumps(response))

