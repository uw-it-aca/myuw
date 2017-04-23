import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.enrollment import (get_current_quarter_enrollment,
                                 get_main_campus,
                                 get_quarter_enrollment)
from myuw.dao.gws import is_grad_student, is_student
from myuw.dao.password import get_pw_json
from myuw.dao.pws import get_display_name_of_current_user
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.user import get_netid_of_current_user
from myuw.dao.term import (get_current_quarter,
                           get_next_quarter,
                           get_next_quarters)
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_msg
from myuw.views import prefetch_resources
from myuw.views.rest_dispatch import RESTDispatch
from restclients_core.exceptions import DataFailureException
from myuw.views.error import data_not_found, handle_exception


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
            prefetch_resources(request,
                               prefetch_enrollment=True,
                               prefetch_password=True)

            netid = get_netid_of_current_user()

            term = get_current_quarter(request)

            if is_student():
                profile = get_profile_of_current_user()
                response = profile.json_data()
                response['is_student'] = True
                response['is_grad_student'] = is_grad_student()

                campuses = get_main_campus(request)
                if 'Seattle' in campuses:
                    response['campus'] = 'Seattle'
                elif 'Tacoma' in campuses:
                    response['campus'] = 'Tacoma'
                elif 'Bothell' in campuses:
                    response['campus'] = 'Bothell'
                try:
                    future_quarters = get_next_quarters(request, 3)
                    enrollments = get_all_enrollments()

                    response['class_level'] = enrollment.class_level

                    response['majors'] = []
                    response['minors'] = []
                    for enrollment in enrollments:
                        current_major = {}
                        current_major['quarter'] = (term.quarter + "-" +
                                                    str(term.year))
                        for major in enrollment.majors:
                            current_major['majors'].append(major.json_data())

                        response['majors'].append(current_major)

                        current_minor = {}
                        current_minor['quarter'] = (term.quarter + "-" +
                                                    str(term.year))
                        for minor in enrollment.minors:
                            current_minor['minors'].append(minor.json_data())

                        response['minors'].append(current_minor)

                except Exception as ex:
                    logger.error(
                        "%s get_current_quarter_enrollment: %s" %
                        (netid, ex))

            else:
                response = {}
                response['is_grad_student'] = False
                response['is_student'] = False
                response['uwnetid'] = netid

            response['display_name'] = get_display_name_of_current_user()

            try:
                response['password'] = get_pw_json(netid, request)
            except Exception as ex:
                logger.error("%s get_pw_json: %s" % (netid, ex))

            log_success_response(logger, timer)
            return HttpResponse(json.dumps(response, default=str))
        except Exception:
            return handle_exception(logger, timer, traceback)
