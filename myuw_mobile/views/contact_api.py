from django.http import HttpResponse
from django.utils import simplejson as json
from rest_dispatch import RESTDispatch
from pws_util import get_contact
import logging

class InstructorContact(RESTDispatch):

    _logger = logging.getLogger('myuw_mobile.views.contact_api.InstructorContact')

    def GET(self, request, regid):
        """ 
        GET returns 200 with the whitepage information of the given person.
        """
        contact = get_contact(regid)
        if not contact:
            return super(InstructorContact, 
                         self).data_not_found(*args, **named_args)

        return HttpResponse(json.dumps(contact))

