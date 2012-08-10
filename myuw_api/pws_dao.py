from django.conf import settings
from restclients.pws_client import PWSClient
import logging
import json
import re

# This module provides the single point access to PWSClient
pws_client = PWSClient()
pws_url_base = 'http://127.0.0.1:8080/identity/v1/'
pws_url_suffix = '/full.json'

uw_directory_url_base = 'https://www.washington.edu/home/peopledir/secure/?method=uwnetid&term='

class Person:
    """ The Person class encapsulates the interactions with the PWS person resource """

    # static class variables
    _logger = logging.getLogger('myuw_api.pws_dao.Person')
    _pws_resource_url = pws_url_base + 'person/'

    def get_regid(self, netid):
        result = pws_client.get_json(Person._pws_resource_url +
                                     netid +
                                     pws_url_suffix)
        if result:
            regid = result['UWRegID']
            if regid and re.match(r'^[A-F0-9]{32}$', regid, re.I):
                return regid
        raise Exception('No valid regid: ' + regid)

    # parameter id: netid or regid
    # return {'inDirectory': True/False,
    #         'directoryUrl': the URL of the UW Directory detail page}
    def get_contact(self, uid):
        contact = {'inDirectory': None,
                   'directoryUrl': None}
        result = pws_client.get_json(Person._pws_resource_url +
                                     uid +
                                     pws_url_suffix)
        if result:
            contact['inDirectory'] = result['WhitepagesPublish']
            if contact['inDirectory'] :
                contact['directoryUrl'] = uw_directory_url_base + result['UWNetID']
            return contact
        raise Exception('Contact not found for ' + uid)

