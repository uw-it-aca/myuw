import logging
from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.affiliation import get_base_campus
from myuw_mobile.dao.enrollment import get_current_quarter_enrollment
from myuw_mobile.dao.student_profile import get_profile_of_current_user
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

        response = profile.json_data()
        response['campus'] = get_base_campus()

        enrollment = get_current_quarter_enrollment()
        if enrollment is not None:
            response['class_level'] = enrollment.class_level
            if len(enrollment.majors) > 0: 
                response['majors'] = []
                for major in enrollment.majors:
                    response['majors'].append(major.json_data())

            if len(enrollment.minors) > 0: 
                response['minors'] = []
                for minor in enrollment.minors:
                    response['minors'].append(minor.json_data())

        logger.debug(response)
        return HttpResponse(json.dumps(response))

