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
    _logger = logging.getLogger('myuw_api.pws_dao.Person')

    def get_regid(self, netid):
        pws = PWS()
        person = pws.get_person_by_netid(netid)

        if person != None:
            return person.uwregid

        raise Exception('No valid regid: ' + regid)

    def get_contact(self, uid):
        # parameter id: netid or regid
        # return {'inDirectory': True/False,
        #         'directoryUrl': the URL of the UW Directory detail page}

        # I don't know what this is, so i'm commenting it out for now
        # It looks like the only caller is also commented out, so i don't
        # feel too bad about that.
        return
#        contact = {'inDirectory': None,
#                   'directoryUrl': None}
#        result = pws_client.get_json(Person._pws_resource_url +
#                                     uid +
#                                     pws_url_suffix)
#        if result:
#            contact['inDirectory'] = result['WhitepagesPublish']
#            if contact['inDirectory'] :
#                contact['directoryUrl'] = uw_directory_url_base +
#                                            result['UWNetID']
#            return contact
#        raise Exception('Contact not found for ' + uid)
