from django.http import HttpResponse
from django.utils import simplejson as json
from rest_dispatch import RESTDispatch, invalid_arg, data_not_found
from myuw_mobile.dao.pws import Person as PersonDao
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.util import log_invalid_regid_response, log_data_not_found_response, log_success_response
import logging

class InstructorContact(RESTDispatch):
    """
    Performs actions on resource at /api/v1/person/.
    """

    def GET(self, request, regid):
        """ 
        GET returns 200 with the whitepage information of the given person.
        """

        timer = Timer()
        logger = logging.getLogger('myuw_mobile.views.contact_api.InstructorContact.GET')

        if not regid:
            log_invalid_regid_response(logger, timer)
            return invalid_arg()

        contact = PersonDao().get_contact(regid)
        if not contact:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        return HttpResponse(json.dumps(contact))

