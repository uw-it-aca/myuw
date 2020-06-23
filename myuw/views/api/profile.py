import logging
import traceback
from myuw.dao import get_netid_of_current_user
from myuw.dao.gws import is_student, is_applicant
from myuw.dao.pws import get_display_name_of_current_user
from myuw.dao.password import get_pw_json
from myuw.dao.student_profile import get_applicant_profile, get_student_profile
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call, log_exception
from myuw.views import prefetch_resources
from myuw.views.api import ProtectedAPI
from restclients_core.exceptions import DataFailureException
from myuw.views.error import data_not_found, handle_exception

logger = logging.getLogger(__name__)


class MyProfile(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/profile/.
    """

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the student account balances
        of the current user
        """
        timer = Timer()
        try:
            netid = get_netid_of_current_user(request)
            prefetch_resources(request,
                               prefetch_group=True,
                               prefetch_enrollment=True,
                               prefetch_password=True,
                               prefetch_sws_person=True)

            if is_student(request):
                response = get_student_profile(request)
            elif is_applicant(request):
                response = get_applicant_profile(request)
            else:
                response = {}
                response['is_grad_student'] = False
                response['is_student'] = False
                response['uwnetid'] = netid

            response['display_name'] = get_display_name_of_current_user(
                request)

            try:
                response['password'] = get_pw_json(request)
            except Exception:
                log_exception(logger, "get_password({0})".format(netid),
                              traceback)

            log_api_call(timer, request, "Get Applicant/Student Profile")
            return self.json_response(response)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)
