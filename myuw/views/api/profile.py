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

    def is_pending(self, pending, current, added):
        """
        Sorts through the current and added pending Major/Minors and
        returns True if the Major/Minor is not either current or already
        added.
        """
        # Obj can be either a SWS Major or Minor object
        for obj in current:
            if pending.full_name == obj['full_name']:
                return False

        for obj in added:
            if pending.full_name == obj.full_name:
                return False

        return True

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

            try:
                term = get_current_quarter(request)
            except Exception as ex:
                print ex

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
                    enrollment = get_current_quarter_enrollment(request)
                    future_enrollments = get_next_quarters(request, 3)

                    response['class_level'] = enrollment.class_level
                    if len(enrollment.majors) > 0:
                        response['majors'] = []
                        for major in enrollment.majors:
                            response['majors'].append(major.json_data())

                    if len(enrollment.minors) > 0:
                        response['minors'] = []
                        for minor in enrollment.minors:
                            response['minors'].append(minor.json_data())

                    response['future_majors'] = []
                    response['future_minors'] = []
                    pending_majors = []
                    pending_minors = []

                    for quarter in future_enrollments:
                        try:
                            enrollment = get_quarter_enrollment(quarter)
                        except DataFailureException:
                            continue

                        major_entry = {}
                        major_entry['majors'] = []
                        major_entry['quarter'] = quarter.quarter

                        for major in enrollment.majors:
                            print major.full_name
                            if self.is_pending(major, response['majors'],
                                               pending_majors):
                                major_entry['majors'].append(major.json_data())
                                pending_majors.append(major)

                        if len(major_entry['majors']) > 0:
                            response['future_majors'].append(major_entry)

                        minor_entry = {}
                        minor_entry['minors'] = []
                        minor_entry['quarter'] = quarter.quarter
                        for minor in enrollment.minors:
                            if self.is_pending(minor, response['minors'],
                                               pending_minors):
                                minor_entry['minors'].append(minor.json_data())
                                pending_minors.append(minor)

                        if len(minor_entry['minors']) > 0:
                            response['future_minors'].append(minor_entry)

                    response['has_pending'] = (len(pending_minors) > 0 and
                                               len(pending_majors) > 0)

                except Exception as ex:
                    import traceback; traceback.print_exc()
                    print ex
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
