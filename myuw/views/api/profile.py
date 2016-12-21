import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.user import get_netid_of_current_user
from myuw.dao.affiliation import get_base_campus
from myuw.dao.enrollment import get_current_quarter_enrollment
from myuw.dao.password import get_pw_json
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.gws import is_grad_student, is_student
from myuw.dao.pws import get_display_name_of_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_msg
from myuw.views.rest_dispatch import RESTDispatch, data_not_found,\
    handle_exception


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
        netid = get_netid_of_current_user()
        try:
            if is_student():
                profile = get_profile_of_current_user()
                response = profile.json_data()
                response['display_name'] = get_display_name_of_current_user()
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
            else:
                response = {}
                response['display_name'] = get_display_name_of_current_user()
                response['is_grad_student'] = False

            try:
                response['password'] = get_pw_json(netid, request)
            except Exception as ex:
                logger.error("get_pw_json(%s): %s" % (netid, ex))
                pass

            log_success_response(logger, timer)
            return HttpResponse(json.dumps(response, default=str))
        except Exception:
            return handle_exception(logger, timer, traceback)
