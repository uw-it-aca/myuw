import logging
from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch, invalid_arg
from myuw_mobile.views.rest_dispatch import data_not_found
from myuw_mobile.dao.pws import get_contact
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_invalid_regid_response
from myuw_mobile.logger.logresp import log_data_not_found_response
from myuw_mobile.logger.logresp import log_success_response


class InstructorContact(RESTDispatch):
    """
    Performs actions on resource at /api/v1/person/.
    """

    def GET(self, request, regid):
        """
        GET returns 200 with the whitepage information of the given person.
        """

        timer = Timer()
        logger = logging.getLogger(__name__)

        if not regid:
            log_invalid_regid_response(logger, timer)
            return invalid_arg()

        contact = get_contact(regid)
        if not contact:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        return HttpResponse(json.dumps(contact))
