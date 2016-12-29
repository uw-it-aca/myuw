import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.affiliation import affiliation_prefetch
from myuw.dao.enrollment import (get_current_quarter_enrollment,
                                 get_main_campus,
                                 enrollment_prefetch)
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.term import current_terms_prefetch
from myuw.dao.gws import is_grad_student
from myuw.dao.pws import get_display_name_of_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_msg
from myuw.util.thread import PrefetchThread
from myuw.views import prefetch
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
        prefetch_profile_resources(request)
        try:
            profile = get_profile_of_current_user()
            response = profile.json_data()
            response['display_name'] = get_display_name_of_current_user()

            campuses = get_main_campus(request)

            if 'Seattle' in campuses:
                response['campus'] = 'Seattle'
            elif 'Tacoma' in campuses:
                response['campus'] = 'Tacoma'
            elif 'Bothell' in campuses:
                response['campus'] = 'Bothell'
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
            return handle_exception(logger, timer, traceback)


def prefetch_profile_resources(request):
    prefetch_methods = []
    prefetch_methods.extend(affiliation_prefetch())
    prefetch_methods.extend(current_terms_prefetch(request))
    prefetch_methods.extend(enrollment_prefetch())

    prefetch(request, prefetch_methods)
