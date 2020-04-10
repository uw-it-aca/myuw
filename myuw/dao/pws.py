"""
This module encapsulates the interactions with the uw_pws,
provides information of the current user
"""

import logging
from uw_pws import PWS, Person
from restclients_core.exceptions import DataFailureException
from myuw.dao import get_netid_of_current_user
from myuw.dao.exceptions import (
    IndeterminateCampusException, UserNotFoundInPws)


#
# mailstop campus range limits as set by UW Mailing Services
#
MAILSTOP_MIN_TACOMA = 358400
MAILSTOP_MAX_TACOMA = 358499
MAILSTOP_MIN_BOTHELL = 358500
MAILSTOP_MAX_BOTHELL = 358599
pws = PWS()
logger = logging.getLogger(__name__)


def get_person_by_employee_id(employee_id):
    return pws.get_person_by_employee_id(employee_id)


def get_person_by_regid(regid):
    return pws.get_person_by_regid(regid)


def get_person_of_current_user(request):
    """
    Retturn a pws Person object with the netid of the current user,
    If no Person exists return a pws Entity object
    """
    if not hasattr(request, "myuw_pws_person"):
        netid = get_netid_of_current_user(request)
        try:
            request.myuw_pws_person = pws.get_person_by_netid(netid)
        except DataFailureException as err:
            if err.status == 404:  # Non-personal
                try:
                    request.myuw_pws_person = pws.get_entity_by_netid(netid)
                except DataFailureException as ex:
                    if ex.status == 404:
                        raise UserNotFoundInPws(ex)
                    raise
            else:
                raise
    return request.myuw_pws_person


def person_prefetch():
    def _method(request):
        return get_person_of_current_user(request)
    return [_method]


def get_display_name_of_current_user(request):
    person = get_person_of_current_user(request)
    return person.display_name


def get_regid_of_current_user(request):
    person = get_person_of_current_user(request)
    return person.uwregid


def get_employee_id_of_current_user(request):
    person = get_person_of_current_user(request)
    if isinstance(person, Person):
        return person.employee_id
    return None


def get_student_number_of_current_user(request):
    person = get_person_of_current_user(request)
    if isinstance(person, Person):
        return person.student_number
    return None


def get_student_system_key_of_current_user(request):
    person = get_person_of_current_user(request)
    if isinstance(person, Person):
        return person.student_system_key
    return None


def is_alumni(request):
    person = get_person_of_current_user(request)
    return (isinstance(person, Person) and
            person.is_alum is True and
            person.is_alum_state_current())


def is_employee(request):
    """
    Current faculty, staff, and student employees
    """
    person = get_person_of_current_user(request)
    return (isinstance(person, Person) and
            person.is_employee is True and
            person.is_emp_state_current())


def is_student(request):
    """
    Return true if the user is an
    UW undergraduate/graduate/onleave graduate/pce students
    who are enrolled for the current quarter,
    the previous quarter, or a future quarter
    """
    person = get_person_of_current_user(request)
    return isinstance(person, Person) and person.is_student is True


def is_faculty(request):
    """
    UW faculty members who are currently employed.
    """
    person = get_person_of_current_user(request)
    return isinstance(person, Person) and person.is_faculty is True


def is_bothell_employee(request):
    person = get_person_of_current_user(request)
    if isinstance(person, Person) and person.mailstop:
        mailstop = int(person.mailstop)
        return MAILSTOP_MIN_BOTHELL <= mailstop <= MAILSTOP_MAX_BOTHELL
    return False


def is_tacoma_employee(request):
    person = get_person_of_current_user(request)
    if isinstance(person, Person) and person.mailstop:
        mailstop = int(person.mailstop)
        return MAILSTOP_MIN_TACOMA <= mailstop <= MAILSTOP_MAX_TACOMA
    return False


def is_seattle_employee(request):
    person = get_person_of_current_user(request)
    return (isinstance(person, Person) and person.mailstop and
            not is_tacoma_employee(request) and
            not is_bothell_employee(request))


def is_prior_employee(request):
    person = get_person_of_current_user(request)
    return isinstance(person, Person) and person.is_emp_state_prior()


def is_prior_student(request):
    person = get_person_of_current_user(request)
    return (isinstance(person, Person) and
            person.is_stud_state_prior() and
            is_student(request) is False)


def is_retiree(request):
    person = get_person_of_current_user(request)
    return isinstance(person, Person) and person.is_retiree()


def get_url_key_for_regid(regid):
    # XXX - I want a hook to obscure/encrypt this down the road
    return regid


def get_regid_for_url_key(key):
    return key


def get_idcard_photo(regid):
    return pws.get_idcard_photo(regid)
    pass


def get_employee_campus(request):
    """
    determine based on mailstop ranges supplied by
    UW Campus Mailing Services mailserv@uw.edu
    """
    if is_tacoma_employee(request):
        return 'Tacoma'
    if is_bothell_employee(request):
        return 'Bothell'
    if is_seattle_employee(request):
        return 'Seattle'
    raise IndeterminateCampusException()
