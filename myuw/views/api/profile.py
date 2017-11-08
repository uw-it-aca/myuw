import logging
import traceback

from myuw.dao.student_profile import get_applicant_profile
from myuw.dao.gws import is_student, is_applicant
from myuw.dao.student_profile import get_student_profile
from myuw.dao.password import get_pw_json
from myuw.dao.pws import get_display_name_of_current_user
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.user import get_netid_of_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_msg
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
            prefetch_resources(request,
                               prefetch_enrollment=True,
                               prefetch_password=True)

            netid = get_netid_of_current_user()

            if is_student():
                response = get_student_profile(request)
            elif is_applicant():
                response = get_applicant_profile(request)
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

            print response

            log_success_response(logger, timer)
            return self.json_response(response)
        except Exception as ex:
            print ex
            return handle_exception(logger, timer, traceback)
