import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.affiliation import get_base_campus
from myuw.dao.enrollment import get_current_quarter_enrollment
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.gws import is_grad_student
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_err, log_msg
from myuw.views.rest_dispatch import RESTDispatch, data_error, data_not_found


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
        try:
            profile = get_profile_of_current_user()
            response = profile.json_data()
            response['campus'] = get_base_campus(request)
            response['is_grad_student'] = is_grad_student()
            try:
                enrollment = get_current_quarter_enrollment(request)
                response['class_level'] = enrollment.class_level
                if len(enrollment.majors) > 0:
                    response['majors'] = []
                    for major in enrollment.majors:
                        response['majors'].append(major.json_data())

                if len(enrollment.minors) > 0:
                    response['minors'] = []
                    for minor in enrollment.minors:
                        response['minors'].append(minor.json_data())
            except Exception:
                pass
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(response))
        except Exception:
            log_err(logger, timer, traceback.format_exc())
            return data_error()
