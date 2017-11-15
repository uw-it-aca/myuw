"""
This module provides affiliations of the current user
"""

import logging
import traceback
from django.conf import settings
from myuw.logger.logback import log_info
from myuw.dao import get_netid_of_current_user
from myuw.dao.schedule import get_current_quarter_schedule
from myuw.dao.pws import get_campus_of_current_user
from myuw.dao.gws import is_grad_student, is_student, \
    is_current_graduate_student, is_undergrad_student, \
    is_pce_student, is_student_employee, is_employee, is_faculty, \
    is_seattle_student, is_bothell_student, is_tacoma_student, \
    is_staff_employee, is_applicant
from myuw.dao.instructor_schedule import is_instructor
from myuw.dao.uwnetid import is_clinician, is_2fa_permitted, get_subscriptions
from myuw.dao.enrollment import get_main_campus
from myuw.dao.thrive import get_target_group, is_fyp, is_aut_transfer,\
    is_win_transfer
from myuw.dao.exceptions import IndeterminateCampusException


logger = logging.getLogger(__name__)


def get_all_affiliations(request):
    """
    return a dictionary of affiliation indicators.
    ["student"]: True if the user is currently an UW student.
    ["grad"]: True if the user is currently an UW graduate student.
    ["undergrad"]: True if the user is currently an UW undergraduate student.
    ["applicant"]: True if the user is currently a UW applicant
    ["pce"]: True if the user is currently an UW PCE student.
    ["employee"]: True if the user is currently a uw employee.
    ["stud_employee"]: True if the user is currently a student employee.
    ["faculty"]: True if the user is currently faculty.
    ["seattle"]: True if the user is an UW Seattle student
                 in the current quarter.
    ["bothell"]: True if the user is an UW Bothell student
                 in the current quarter.
    ["tacoma"]: True if the user is an UW Tacoma student
                in the current quarter.
    ["official_seattle"]: True if the user is an UW Seattle student
                 according to the SWS Enrollment.
    ["official_bothell"]: True if the user is an UW Bothell student
                 according to the SWS Enrollment.
    ["official_tacoma"]: True if the user is an UW Tacoma student
                according to the SWS Enrollment.
    ["official_pce"]: True if the user is an UW PCE student
                according to the SWS Enrollment.
    """

    if hasattr(request, 'myuw_user_affiliations'):
        return request.myuw_user_affiliations

    data = {"grad": is_grad_student(),
            "undergrad": is_undergrad_student(),
            "applicant": is_applicant(),
            "student": is_student(),
            "pce": is_pce_student(),
            "staff_employee": is_staff_employee(),
            "stud_employee": is_student_employee(),
            "employee": is_employee(),
            "fyp": is_fyp(request),
            "aut_transfer": is_aut_transfer(request),
            "win_transfer": is_win_transfer(request),
            "faculty": is_faculty(),
            "clinician": is_clinician(),
            "is_2fa_permitted": is_2fa_permitted(),
            "instructor": is_instructor(request),
            "seattle": is_seattle_student(),
            "bothell": is_bothell_student(),
            "tacoma": is_tacoma_student(),
            }

    # add 'official' campus info
    campuses = []
    try:
        campuses = get_main_campus(request)
    except IndeterminateCampusException:
        try:
            campuses = [get_campus_of_current_user()]
        except IndeterminateCampusException:
            pass

    official_campuses = _get_official_campuses(campuses)
    data = dict(data.items() + official_campuses.items())
    # Note:
    #    As the UW Affiliation group (gws) only knows about one campus,
    #    we use registered sections in the current quarter
    #    to determine the campuses.
    log_info(logger, data)
    request.myuw_user_affiliations = data
    return data


def _get_campuses_by_schedule(schedule):
    """
    Returns a dictionary indicating the campuses that the student
    has enrolled in the given schedule:
     { seattle: false|true,
       bothell: false|true,
       tacoma: false|true }
    True if the user is registered on that campus.
    """
    campuses = {"seattle": False,
                "bothell": False,
                "tacoma": False,
                "pce": False}

    if schedule is not None and len(schedule.sections) > 0:
        for section in schedule.sections:
            if section.course_campus == "Seattle":
                campuses["seattle"] = True
            elif section.course_campus == "Bothell":
                campuses["bothell"] = True
            elif section.course_campus == "Tacoma":
                campuses["tacoma"] = True
            elif section.course_campus == "PCE":
                campuses["pce"] = True
            else:
                pass
    return campuses


def _get_official_campuses(campuses):
    official_campuses = {'official_seattle': False,
                         'official_bothell': False,
                         'official_tacoma': False,
                         'official_pce': False}
    for campus in campuses:
        if campus.lower() == "seattle":
            official_campuses['official_seattle'] = True
        if campus.lower() == "tacoma":
            official_campuses['official_tacoma'] = True
        if campus.lower() == "bothell":
            official_campuses['official_bothell'] = True
        if campus.lower() == "pce":
            official_campuses['official_pce'] = True
    return official_campuses


def get_base_campus(request):
    """
    Return one currently enrolled campus.
    If not exist, return one affiliated campus.
    """
    campus = ""
    affiliations = get_all_affiliations(request)
    try:
        if affiliations["official_seattle"]:
            campus = "seattle"
        if affiliations["official_bothell"]:
            campus = "bothell"
        if affiliations["official_tacoma"]:
            campus = "tacoma"
        if affiliations["official_pce"]:
            campus = "pce"
    except KeyError:
        try:
            if affiliations["seattle"]:
                campus = "seattle"
            if affiliations["bothell"]:
                campus = "bothell"
            if affiliations["tacoma"]:
                campus = "tacoma"
        except KeyError:
            campus = ""
            pass
    return campus


def _build_cache_method(name, method):
    name = "myuw_cache_%s" % name

    def generated(request):
        if hasattr(request, name):
            return getattr(request, name)
        value = method()
        setattr(request, name, value)
        return value
    return generated


request_cached_is_grad_student = _build_cache_method("grad_student",
                                                     is_grad_student)


request_cached_is_undergrad = _build_cache_method("undergrad",
                                                  is_undergrad_student)


request_cached_is_student = _build_cache_method("student",
                                                is_student)


request_cached_is_pce_student = _build_cache_method("pce_student",
                                                    is_pce_student)


request_cached_is_student_employee = _build_cache_method("student_employee",
                                                         is_student_employee)


request_cached_is_employee = _build_cache_method("student_employee",
                                                 is_employee)


request_cached_is_staff_employee = _build_cache_method("staff_employee",
                                                       is_staff_employee)


request_cached_is_faculty = _build_cache_method("faculty",
                                                is_faculty)


def wrapped_is_seattle(request):
    return is_seattle_student()


def wrapped_is_tacoma(request):
    return is_tacoma_student()


def wrapped_is_bothell(request):
    return is_bothell_student()


def wrapped_get_subscriptions(request):
    return get_subscriptions()


def wrapped_is_instructor(request):
    return is_instructor(request)


def affiliation_prefetch():
    return [request_cached_is_grad_student,
            request_cached_is_undergrad,
            request_cached_is_student,
            request_cached_is_pce_student,
            request_cached_is_student_employee,
            request_cached_is_staff_employee,
            request_cached_is_employee,
            request_cached_is_faculty,
            wrapped_is_seattle,
            wrapped_is_tacoma,
            wrapped_is_bothell,
            wrapped_get_subscriptions,
            wrapped_is_instructor,
            ]


def get_identity_log_str(request):
    """
    Return "(Affiliations: <affiliations>, <campus codes>)"
    """
    res = "(Affiliations:"
    no_affiliation_lengthmark = len(res)
    affi = get_all_affiliations(request)
    if affi["grad"]:
        res += ' Grad'
    if affi["undergrad"]:
        res += ' Undergrad'
    if affi["pce"]:
        res += ' PCE-student'
    if affi["faculty"]:
        res += ' Faculty'
    if affi["staff_employee"]:
        res += ' Staff'
    if affi["instructor"]:
        res += ' Instructor'
    if affi["clinician"]:
        res += 'Clinician'
    if affi["employee"]:
        res += ' Employee'
    if len(res) == no_affiliation_lengthmark:
        res += 'None'

    res += ', Campuses:'
    no_campus_lengthmark = len(res)
    if affi["seattle"] or affi["official_seattle"]:
        res += ' Seattle'
    if affi["bothell"] or affi["official_bothell"]:
        res += ' Bothell'
    if affi["tacoma"] or affi["official_tacoma"]:
        res += ' Tacoma'
    if affi["official_pce"]:
        res += ' PCE'
    if len(res) == no_campus_lengthmark:
        res += 'None'
    res += ') '
    return res
