from django.conf import settings
from restclients.pws_client import PWSClient
import logging
import json
import re


class Person:
    """ The Person class encapsulates the interactions with the PWS client """

    __logger = logging.getLogger('myuw_api.person')
    __pws_client = PWSClient()

    def get_regid(self, netid):
        return '9136CCB8F66711D5BE060004AC494FFE'
#        regid = __pws_client.get_person_by_netid(netid).uwregid
#        if not re.match(r'^[A-F0-9]{32}$', regid, re.I):
#            raise InvalidRegid("Invalid regid: " + regid)
#       return regid

    def get_contact(self, regid):
        pass
#        self.person = __pws_client.get_person_by_regid(netid)
# validate return attributes 
#        return {'email':
#                 'phone':
#                 }        


class InvalidRegid(RuntimeError):
    def __init__(self, arg):
        self.args = arg
