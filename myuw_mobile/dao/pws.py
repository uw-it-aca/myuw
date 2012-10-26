from django.conf import settings
import logging
import traceback
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
        """
        Retrieve the person data using the netid of the user
        """
        timer = Timer()
        try:
            netid = UserService().get_user()
            return PWS().get_person_by_netid(netid)
        except Exception as ex:
            log_exception(Person._logger, 
                          'pws.get_person_by_netid', 
                          traceback.format_exc())
        finally:
            log_resp_time(Person._logger, 
                          'pws.get_person_by_netid', 
                          timer)
        return None

    def is_student(self):
        """
        Return true if the user is an 
        UW undergraduate/graduate/onleave graduate/pce students 
        who are enrolled for the current quarter, 
        the previous quarter, or a future quarter
        """
        res = self._get_person()
        if res is not None:
            return res.is_student
        return None

    def get_regid(self):
        res = self._get_person()
        if res is not None:
            return res.uwregid
        return None

    def get_contact(self, regid):
        """
        Return the whitepage information if the user has given 
        permission to publish it on the UW Directory.
        """
        contact = None
        timer = Timer()
        try:
            contact = PWS().get_contact(regid)
        except Exception as ex:
            log_exception(Person._logger, 
                          'pws.get_contact for ' + regid, 
                          traceback.format_exc())
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


