from django.conf import settings
import traceback
import logging
import sys
from restclients.pws import PWS

pws = PWS()

class Person:
    """
    The Person class encapsulates the interactions
    with the PWS person resource
    """

    # static class variables
    _logger = logging.getLogger('myuw_mobile.dao.pws.Person')

    def get_person_by_netid(self, netid):
        try:
            return pws.get_person_by_netid(netid)
        except Exception, message:
            print 'Failed to get person: ', message
            traceback.print_exc(file=sys.stdout)
            Person._logger.error("Ex: get_person_by_netid for " + 
                                 netid + " --> " + message)
            return None



    def is_student(self, netid):
        return self.get_person_by_netid(netid).is_student


    def get_regid(self, netid):
        return self.get_person_by_netid(netid).uwregid


    def get_contact(self, regid):
        try:
            contact = pws.get_contact(regid)
        except Exception, message:
            print 'Failed to get instructor data: ', message
            traceback.print_exc(file=sys.stdout)
            Person._logger.error("Ex: get_contact for "+
                                 regid + " --> " + message)
            return None

        if not contact:
            return None

        if not contact["WhitepagesPublish"] :
            affiliations = contact["PersonAffiliations"]
            if "EmployeePersonAffiliation" in affiliations:
                data = affiliations["EmployeePersonAffiliation"]
                data["EmployeeWhitePages"] = {}

            if "StudentPersonAffiliation" in affiliations:
                data = affiliations["StudentPersonAffiliation"]
                data["StudentWhitePages"] = {}

        return contact                


