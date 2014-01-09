from django.conf import settings
import logging
import traceback
from restclients.pws import PWS
from userservice.user import UserService
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception, log_info

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

    def _get_contact(self, regid):
        """
        Return the raw contact information of the given user
        """
        contact = None
        timer = Timer()
        try:
            contact = PWS().get_contact(regid)
            #log_info(Person._logger, contact)
        except Exception as ex:
            log_exception(Person._logger, 
                          'pws.get_contact for ' + regid, 
                          traceback.format_exc())
        finally:
            log_resp_time(Person._logger, 
                          'pws.get_contact for ' + regid, 
                          timer)
        return contact

    def _get_cur_user_contact(self):
        """
        Return the raw contact information of the current user
        """
        regid = self.get_regid()
        if regid is None:
            return None
        return self._get_contact(regid)

    def get_contact(self, regid):
        """
        Return the whitepage information of the user if she
        gives permission to publish it on the UW Directory.
        """
        contact = self._get_contact(regid)
        if contact is not None and not contact["WhitepagesPublish"] :
            affiliations = contact["PersonAffiliations"]
            if "EmployeePersonAffiliation" in affiliations:
                data = affiliations["EmployeePersonAffiliation"]
                data["EmployeeWhitePages"] = {}

            if "StudentPersonAffiliation" in affiliations:
                data = affiliations["StudentPersonAffiliation"]
                data["StudentWhitePages"] = {}

        return contact                


    def get_student_affi(self):
        """
        Return the student affiliation of the user, None if not exist
        """
        contact = self._get_cur_user_contact()
        if contact is not None and "PersonAffiliations" in contact:
            affi = contact["PersonAffiliations"]
            if "StudentPersonAffiliation" in affi:
                return affi["StudentPersonAffiliation"]
        return None

    def get_student_system_key(self):
        """
        Return the student system key of the user
        """
        studAffi = self.get_student_affi()
        if studAffi is None:
            return None
        return studAffi["StudentSystemKey"]

    def get_student_number(self):
        """
        Return the student number of the user
        """
        studAffi = self.get_student_affi()
        if studAffi is None:
            return None
        return studAffi["StudentNumber"]

    def get_employee_affi(self):
        """
        Return the student affiliation of the user, None if not exist
        """
        contact = self._get_cur_user_contact()
        if contact is not None  and "PersonAffiliations" in contact:
            affi = contact["PersonAffiliations"]
            if "EmployeePersonAffiliation" in affi:
                return affi["EmployeePersonAffiliation"]
        return None

    def get_employee_id(self):
        """
        Return the employee identification number of the current user
        """
        employeeAffi = self.get_employee_affi()
        if employeeAffi is None:
            return None
        return employeeAffi["EmployeeID"]


#def test():
#    person = Person()
#    person._get_contact("6DF0A9206A7D11D5A4AE0004AC494FFE")
#    person._get_contact("9136CCB8F66711D5BE060004AC494FFE")
