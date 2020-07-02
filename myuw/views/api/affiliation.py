import logging
import traceback
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.user import get_updated_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call, log_exception
from myuw.views import prefetch_resources
from myuw.views.error import handle_exception, unknown_uwnetid
from myuw.views.api import ProtectedAPI

logger = logging.getLogger(__name__)


class Affiliation(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        Performs actions on resource at /api/v1/affiliation/.
        GET returns 200 with the current user's affiliation
        @return status 403: no valid authentication token
                status 543: data error
        """
        timer = Timer()
        try:
            person = get_updated_user(request)
        except Exception:
            log_exception(logger, "Affiliation:get_updated_user", traceback)
            return unknown_uwnetid()

        try:
            prefetch_resources(request,
                               prefetch_group=True,
                               prefetch_enrollment=True,
                               prefetch_instructor=True,
                               prefetch_sws_person=True)

            resp = get_all_affiliations(request)
            log_api_call(timer, request, "Get Affiliation")
            request.session.set_expiry(60)
            return self.json_response(resp)
        except Exception:
            handle_exception(logger, timer, traceback)
