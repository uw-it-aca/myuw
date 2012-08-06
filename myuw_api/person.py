from django.conf import settings
from restclients.pws_client import PWSClient
import logging
import json

class Person:
    """ The Person class encapsulate the access to the Term data """

    __logger = logging.getLogger('myuw_api.person')
    __pws_client = PWSClient()

    def get_regid(self, netid):
        return '9136CCB8F66711D5BE060004AC494FFE'
#       self.person = __pws_client.get_person_by_netid(netid)
#       return self.person.uwregid

    def get_contact(self, regid):
#        self.person = __pws_client.get_person_by_regid(netid)
#        return {'email':
#                 'phone':
#                 }        
        pass
