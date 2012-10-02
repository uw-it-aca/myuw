from django.conf import settings
import traceback
import logging
import sys
from restclients.pws import PWS
from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer

pws = PWS()

class Person:
    """
    The Person class encapsulates the interactions
    with the PWS person resource
    """

    # static class variables
    _logger = logging.getLogger('myuw_mobile.dao.pws.Person')

    def __init__(self, user_service):
        self._user_service = user_service
        self._netid = user_service.get_user()

    def get_person_by_netid(self):
        timer = Timer()
        try:
            return pws.get_person_by_netid(self._netid)
        except Exception, message:
            print 'Failed to get person data: ', message
            traceback.print_exc()
            Person._logger.error("get_person_by_netid %s %s", 
                                 Exception, message,
                                 self._user_service.get_log_user_info())
        finally:
            Person._logger.info("PWS get_person_by_netid time=%s", 
                                timer.get_elapsed(),
                                self._user_service.get_log_user_info())
        return None

    def is_student(self):
        return self.get_person_by_netid().is_student

    def get_regid(self):
        return self.get_person_by_netid().uwregid

    def get_contact(self, regid):
        contact = None
        timer = Timer()
        try:
            contact = pws.get_contact(regid)
        except Exception, message:
            print 'Failed to get instructor data: ', message
            traceback.print_exc()
            Person._logger.error("get_contact for %s: %s %s", 
                                 regid, Exception, message,
                                 self._user_service.get_log_user_info())
        finally:
            Person._logger.info("PWS get_contact for %s time=%s", 
                                regid, timer.get_elapsed(),
                                self._user_service.get_log_user_info())

        if contact and not contact["WhitepagesPublish"] :
            affiliations = contact["PersonAffiliations"]
            if "EmployeePersonAffiliation" in affiliations:
                data = affiliations["EmployeePersonAffiliation"]
                data["EmployeeWhitePages"] = {}

            if "StudentPersonAffiliation" in affiliations:
                data = affiliations["StudentPersonAffiliation"]
                data["StudentWhitePages"] = {}

        return contact                


