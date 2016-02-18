import logging
from django.http import HttpResponse
import json
from myuw.dao.affiliation import get_base_campus
from myuw.dao.enrollment import get_current_quarter_enrollment
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.gws import is_grad_student
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_msg
from myuw.views.rest_dispatch import RESTDispatch, data_not_found, data_error


logger = logging.getLogger(__name__)


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
        profile = get_profile_of_current_user()
        if profile is None:
            log_msg(logger, timer, "Person data error")
            return data_error()

        response = profile.json_data()
        response['campus'] = get_base_campus(request)

        enrollment = get_current_quarter_enrollment(request)
        if enrollment is not None:
            response['is_grad_student'] = is_grad_student()
            response['class_level'] = enrollment.class_level
            if len(enrollment.majors) > 0:
                response['majors'] = []
                for major in enrollment.majors:
                    response['majors'].append(major.json_data())

            if len(enrollment.minors) > 0:
                response['minors'] = []
                for minor in enrollment.minors:
                    response['minors'].append(minor.json_data())

        log_success_response(logger, timer)
        return HttpResponse(json.dumps(response))
