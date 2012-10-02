from django.http import HttpResponse
from django.utils import simplejson as json
from rest_dispatch import RESTDispatch, invalid_arg, data_not_found
from myuw_mobile.dao.pws import Person as PersonDao
from myuw_mobile.user import UserService
import logging

class InstructorContact(RESTDispatch):

    _logger = logging.getLogger('myuw_mobile.views.contact_api.InstructorContact')

    def GET(self, request, regid):
        """ 
        GET returns 200 with the whitepage information of the given person.
        """

        user_service = UserService(request)
        if not regid:
            return invalid_arg()

        contact = PersonDao(user_service).get_contact(regid)
        if not contact:
            return data_not_found()

        return HttpResponse(json.dumps(contact))

