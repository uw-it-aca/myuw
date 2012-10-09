from django.conf import settings
import traceback
import logging
import sys
from restclients.pws import PWS
from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception

class Person:
    """
    The Person class encapsulates the interactions
    with the PWS person resource
    """

    # static class variables
    _logger = logging.getLogger('myuw_mobile.dao.pws.Person')

    def _get_person(self):
        timer = Timer()
        try:
            netid = UserService().get_user()
            return PWS().get_person_by_netid(netid)
        except Exception, message:
            traceback.print_exc(file=sys.stdout)
            log_exception(Person._logger, 
                          'pws.get_person_by_netid', 
                          message)
        finally:
            log_resp_time(Person._logger, 
                          'pws.get_person_by_netid', 
                          timer)
        return None

    def is_student(self):
        res = self._get_person()
        if res:
            return res.is_student
        return None

    def get_regid(self):
        res = self._get_person()
        if res:
            return res.uwregid
        return None

    def get_contact(self, regid):
        contact = None
        timer = Timer()
        try:
            contact = PWS().get_contact(regid)
        except Exception, message:
            traceback.print_exc(file=sys.stdout)
            log_exception(Person._logger, 
                          'pws.get_contact for ' + regid, 
                          message)
        finally:
            log_resp_time(Person._logger, 
                          'pws.get_contact for ' + regid, 
                          timer)

        if contact and not contact["WhitepagesPublish"] :
            affiliations = contact["PersonAffiliations"]
            if "EmployeePersonAffiliation" in affiliations:
                data = affiliations["EmployeePersonAffiliation"]
                data["EmployeeWhitePages"] = {}

            if "StudentPersonAffiliation" in affiliations:
                data = affiliations["StudentPersonAffiliation"]
                data["StudentWhitePages"] = {}

        return contact                


