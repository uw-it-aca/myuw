"""
This module encapsulates the interactions with the restclients.pws,
provides information of the current user
"""

from django.conf import settings
import logging
import traceback
from restclients.pws import PWS
from userservice.user import UserService
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception, log_info

logger =  logging.getLogger(__name__)


def get_netid_of_current_user():
    return UserService().get_user()


def _get_person_of_current_user():
    """
    Retrieve the person data using the netid of the current user
    """
    timer = Timer()
    try:
        return PWS().get_person_by_netid(get_netid_of_current_user())
    except Exception as ex:
        log_exception(logger, 
                      'pws.get_person_by_netid', 
                      traceback.format_exc())
    finally:
        log_resp_time(logger, 
                      'pws.get_person_by_netid', 
                      timer)
    return None


def get_regid_of_current_user():
    """
    Return the regid of the current user
    """
    res = _get_person_of_current_user()
    if res is not None:
        return res.uwregid


def _get_contact_by_regid(regid):
    """
    Return the raw contact information of the given regid
    """
    timer = Timer()
    try:
        return PWS().get_contact(regid)
    except Exception as ex:
        log_exception(logger, 
                      'pws.get_contact for ' + regid, 
                      traceback.format_exc())
    finally:
        log_resp_time(logger, 
                      'pws.get_contact for ' + regid, 
                      timer)
    return None


def _get_contact_of_current_user():
    """
    Return the raw contact information of the current user
    """
    regid = get_regid_of_current_user()
    if regid is not None:
        return _get_contact_by_regid(regid)


def get_contact(regid):
    """
    Return the whitepage information of the user if she
    gives permission to publish it on the UW Directory.
    """
    contact = _get_contact_by_regid(regid)
    if contact is not None and not contact["WhitepagesPublish"] :
        affiliations = contact["PersonAffiliations"]
        if "EmployeePersonAffiliation" in affiliations:
            data = affiliations["EmployeePersonAffiliation"]
            data["EmployeeWhitePages"] = {}

        if "StudentPersonAffiliation" in affiliations:
            data = affiliations["StudentPersonAffiliation"]
            data["StudentWhitePages"] = {}

    return contact                


def get_student_affi():
    """
    Return the student affiliation of the user, None if not exist
    """
    contact = _get_contact_of_current_user()
    if contact is not None and "PersonAffiliations" in contact:
        affi = contact["PersonAffiliations"]
        if "StudentPersonAffiliation" in affi:
            return affi["StudentPersonAffiliation"]


def get_student_system_key():
    """
    Return the student system key of the user
    """
    studAffi = get_student_affi()
    if studAffi is not None:
        return studAffi["StudentSystemKey"]


def get_student_number():
    """
    Return the student number of the user
    """
    studAffi = get_student_affi()
    if studAffi is not None:
        return studAffi["StudentNumber"]


def get_employee_affi():
    """
    Return the student affiliation of the user, None if not exist
    """
    contact = _get_contact_of_current_user()
    if contact is not None  and "PersonAffiliations" in contact:
        affi = contact["PersonAffiliations"]
        if "EmployeePersonAffiliation" in affi:
            return affi["EmployeePersonAffiliation"]


def get_employee_id():
    """
    Return the employee identification number of the current user
    """
    employeeAffi = get_employee_affi()
    if employeeAffi is not None:
        return employeeAffi["EmployeeID"]


def is_student():
    """
    Return true if the user is an 
    UW undergraduate/graduate/onleave graduate/pce students 
    who are enrolled for the current quarter, 
    the previous quarter, or a future quarter
    """
    res = _get_person_of_current_user()
    if res is not None:
        return res.is_student

