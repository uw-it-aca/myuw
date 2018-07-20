"""
This module provides affiliations of the current user
"""

import logging
from myuw.dao.enrollment import get_main_campus, get_class_level
from myuw.dao.gws import is_alumni, is_alum_asso, is_regular_employee,\
    is_student, is_grad_student, is_undergrad_student,\
    is_pce_student, is_student_employee, is_staff_employee,\
    is_seattle_student, is_bothell_student, is_tacoma_student,\
    is_applicant, is_grad_c2, is_undergrad_c2, no_major_affiliations
from myuw.dao.instructor import is_instructor
from myuw.dao.pws import get_employee_campus, is_employee
from myuw.dao.term import get_current_quarter
from myuw.dao.thrive import is_fyp, is_aut_transfer, is_win_transfer
from myuw.dao.uwnetid import is_clinician, is_2fa_permitted, is_faculty,\
    is_past_grad, is_past_undergrad, is_past_pce, is_retired_staff,\
    is_past_clinician, is_past_faculty, is_past_staff
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.exceptions import IndeterminateCampusException


logger = logging.getLogger(__name__)


def get_all_affiliations(request):
    """
    return a dictionary of affiliation indicators.

    The first class affiliations:
    ["employee"]: True if the user is currently a uw employee.
    ["faculty"]: True if the user is currently faculty.
    ["staff_employee"]: True if the user is currently staff.
    ["student"]: True if the user is currently an UW student.
    ["stud_employee"]: True if the user is currently a student employee.
    ["grad"]: True if the user is currently an UW graduate student.
    ["undergrad"]: True if the user is currently an UW undergraduate student.
    ["applicant"]: True if the user is currently a UW applicant
    ["pce"]: True if the user is an UW PCE student.
    ["grad_c2"]: True if the user takes UW PCE grad courses
    ["undergrad_c2"]: True if the user takes UW PCE undergrad courses

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
    ["official_pce"]: waiting on sws to add a field in Enrollment.
    ["alum_asso"]: alumni association member
    ["class_level"]: current term class level
    ["F1"]: F1 international student
    ["J1"]: J1 international student
    ["intl_stud"]: F1 or J1 international student
    ["no_1st_class_affi"]: not applicant, employee, student, instructor

    The following are secondary affiliations (without 1st_class_aff):
    ["alumni"]: True if the user is currently an UW alumni and NOT
                current student, employee, applicant
    ["retiree"]: True if the user is a retired staff  and NOT
                current applicant, student, employee
    ["past_employee"]: True if the user is a former employee and NOT
                       current student, applicant
    ["past_stud"]: True if the user is a former student and NOT
                   current employee, applicant
    """
    if hasattr(request, 'myuw_user_affiliations'):
        return request.myuw_user_affiliations

    not_major_affi = no_major_affiliations(request)
    (is_aut_xfer, is_fy_stud, is_win_xfer, is_sea_stud,
     is_undergrad, is_hxt_viewer) = get_is_hxt_viewer(request)
    data = {"class_level": None,
            "grad": is_grad_student(request),
            "undergrad": is_undergrad,
            "applicant": is_applicant(request),
            "student": is_student(request),
            "pce": is_pce_student(request),
            "grad_c2": is_grad_c2(request),
            "undergrad_c2": is_undergrad_c2(request),
            "F1": False,
            "J1": False,
            "intl_stud": False,
            "staff_employee": is_staff_employee(request),
            "stud_employee": is_student_employee(request),
            "employee": is_regular_employee(request),
            "fyp": is_fy_stud,
            "aut_transfer": is_aut_xfer,
            "win_transfer": is_win_xfer,
            "faculty": is_faculty(request),
            "clinician": is_clinician(request),
            "2fa_permitted": is_2fa_permitted(request),
            "instructor": is_instructor(request),
            "seattle": is_sea_stud,
            "bothell": is_bothell_student(request),
            "tacoma": is_tacoma_student(request),
            "hxt_viewer": is_hxt_viewer,
            "alum_asso": is_alum_asso(request),
            "alumni": is_alumni(request) and not_major_affi,
            "retiree": is_retired_staff(request) and not_major_affi,
            "past_employee": (is_past_staff(request) or
                              is_past_faculty(request) or
                              is_past_clinician(request)) and not_major_affi,
            "past_stud": (is_past_grad(request) or
                          is_past_undergrad(request) or
                          is_past_pce(request)) and not_major_affi,
            "no_1st_class_affi": not_major_affi,
            }

    campuses = []

    if data["student"]:
        data["class_level"] = get_class_level(request)

        try:
            sws_person = get_profile_of_current_user(request)
            data["F1"] = sws_person.is_F1()
            data["J1"] = sws_person.is_J1()
            data["intl_stud"] = data["F1"] or data["J1"]
        except Exception as ex:
            logger.error(ex)

        # determine student campus based on current and future enrollments
        try:
            campuses = get_main_campus(request)
        except IndeterminateCampusException:
            pass

    if len(campuses) == 0 and is_employee(request):
        # determine employee primary campus based on their mailstop
        try:
            campuses = [get_employee_campus(request)]
        except IndeterminateCampusException:
            pass

    data.update(_get_official_campuses(campuses))
    request.myuw_user_affiliations = data
    return data


def _get_official_campuses(campuses):
    official_campuses = {'official_seattle': False,
                         'official_bothell': False,
                         'official_tacoma': False}
    if 'Bothell' in campuses:
        official_campuses['official_bothell'] = True
    if 'Seattle' in campuses:
        official_campuses['official_seattle'] = True
    if 'Tacoma' in campuses:
        official_campuses['official_tacoma'] = True
    return official_campuses


def get_base_campus(affiliations):
    """
    Return one currently enrolled campus.
    If not exist, return one affiliated campus.
    """
    campus = ""
    try:
        if affiliations["official_seattle"]:
            campus = "seattle"
        if affiliations["official_bothell"]:
            campus = "bothell"
        if affiliations["official_tacoma"]:
            campus = "tacoma"
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


def get_is_hxt_viewer(request):
    is_fy_stud = is_fyp(request)
    is_aut_xfer = is_aut_transfer(request)
    is_win_xfer = is_win_transfer(request)
    is_sea_stud = is_seattle_student(request)
    is_undergrad = is_undergrad_student(request)
    is_viewer = False
    if is_sea_stud and is_undergrad and not is_fy_stud:
        term = get_current_quarter(request)
        if term.quarter == 'winter':
            is_viewer = not is_win_xfer
        elif term.quarter == 'autumn':
            is_viewer = not is_aut_xfer
        else:
            is_viewer = True
    return (is_aut_xfer, is_fy_stud, is_win_xfer, is_sea_stud,
            is_undergrad, is_viewer)
