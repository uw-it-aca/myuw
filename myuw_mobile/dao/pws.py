from django.conf import settings
from restclients.pws import PWS
import logging
import json
import re


class Person:
    """
    The Person class encapsulates the interactions
    with the PWS person resource
    """

    # static class variables
    _logger = logging.getLogger('myuw_mobile.dao.pws.Person')

    def get_person_by_netid(self, netid):
        pws = PWS()
        person = pws.get_person_by_netid(netid)

        return person

    def get_regid(self, netid):
        pws = PWS()
        person = pws.get_person_by_netid(netid)

        if person != None:
            return person.uwregid

        raise Exception('No valid regid: ' + regid)

    def get_contact(self, regid):
        pws = PWS()
        person = pws.get_contact(regid)
        if person != None:
            return person
        raise Exception('Contact not found for ' + regid)
