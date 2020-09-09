"""
This module provides affiliations of the current user
"""

import logging
import traceback
from myuw.dao import log_err
from myuw.dao.exceptions import IndeterminateCampusException
from myuw.dao.enrollment import (
    get_main_campus, get_class_level, is_registered_current_quarter)
from myuw.dao.gws import (
    is_clinician, is_regular_employee, is_staff_employee, is_student_employee,
    is_alum_asso, is_student, is_grad_student, is_undergrad_student,
    is_pce_student, is_seattle_student, is_bothell_student, is_tacoma_student,
    is_applicant, is_grad_c2, is_undergrad_c2, no_major_affiliations,
    in_fyp_group, in_au_xfer_group, in_wi_xfer_group, in_hxtoolkit_group)
from myuw.dao.instructor import is_instructor
from myuw.dao.pws import (
    get_employee_campus, is_employee, is_faculty, is_prior_employee,
    is_prior_student, is_retiree, is_alumni)
from myuw.dao.term import get_current_quarter
from myuw.dao.uwnetid import is_2fa_permitted
from myuw.dao.student_profile import get_profile_of_current_user

logger = logging.getLogger(__name__)


def get_all_affiliations(request):
    """
    return a dictionary of affiliation indicators.

    The first class affiliations:
    ["employee"]: True if the user is currently a uw employee.
    ["faculty"]: True if the user is currently faculty.
    ["staff_employee"]: True if the user is currently staff.
    ["student"]: True if the user is currently an UW student.
    ["registered_stud"]: True if the student is registered in current quarter.
    ["stud_employee"]: True if the user is currently a student employee.
    ["grad"]: True if the user is currently an UW graduate student.
    ["undergrad"]: True if the user is currently an UW undergraduate student.
    ["applicant"]: True if the user is currently a UW applicant
    ["pce"]: True if the user is an UW PCE student.
    ["grad_c2"]: True if the user takes UW PCE grad courses
    ["undergrad_c2"]: True if the user takes UW PCE undergrad courses

    ["seattle"]: True if the user is an UW Seattle student
    ["bothell"]: True if the user is an UW Bothell student
    ["tacoma"]: True if the user is an UW Tacoma student
    ["official_seattle"]: True if the user is Seattle employee
    ["official_bothell"]: True if the user is Bothell employee
    ["official_tacoma"]: True if the user is Tacoma employee
    ["official_pce"]: waiting on sws to add a field in Enrollment.
    ["class_level"]: current term class level
    ["F1"]: F1 international student
    ["J1"]: J1 international student
    ["intl_stud"]: F1 or J1 international student
    ["hxt_viewer"]: Husky Experience Toolkit viewer
    ["no_1st_class_affi"]: not applicant, employee, student, instructor

    The following are secondary affiliations (without 1st_class_aff):
    ["alumni"]: True if the user is currently an UW alumni and NOT
                current student, employee, applicant
    ["alum_asso"]: alumni association member
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
            "registered_stud": False,
            "pce": is_pce_student(request),
            "grad_c2": is_grad_c2(request),
            "undergrad_c2": is_undergrad_c2(request),
            "F1": False,
            "J1": False,
            "intl_stud": False,
            "fyp": is_fy_stud,
            "aut_transfer": is_aut_xfer,
            "win_transfer": is_win_xfer,
            "2fa_permitted": is_2fa_permitted(request),
            "employee": is_regular_employee(request),
            "faculty": is_faculty(request),
            "clinician": is_clinician(request),
            "instructor": is_instructor(request),
            "staff_employee": is_staff_employee(request),
            "stud_employee": is_student_employee(request),
            "seattle": is_sea_stud,
            "bothell": is_bothell_student(request),
            "tacoma": is_tacoma_student(request),
            "official_seattle": False,
            "official_bothell": False,
            "official_tacoma": False,
            "hxt_viewer": is_hxt_viewer,
            "alum_asso": is_alum_asso(request),
            "alumni": is_alumni(request) and not_major_affi,
            "retiree": is_retiree(request) and not_major_affi,
            "past_employee": is_prior_employee(request) and not_major_affi,
            "past_stud": is_prior_student(request) and not_major_affi,
            "no_1st_class_affi": not_major_affi,
            }

    campuses = []

    if data["student"]:
        data["class_level"] = get_class_level(request)
        data["registered_stud"] = is_registered_current_quarter(request)
        try:
            sws_person = get_profile_of_current_user(request)
            data["F1"] = sws_person.is_F1()
            data["J1"] = sws_person.is_J1()
            data["intl_stud"] = data["F1"] or data["J1"]
        except Exception:
            log_err(logger, "get_profile_of_current_user", traceback, request)

        # enhance student campus with current and future enrollments
        campuses = get_main_campus(request)
        if len(campuses) > 0:
            data["enrolled_stud"] = True
            data['seattle'] = data['seattle'] or ('Seattle' in campuses)
            data['bothell'] = data['bothell'] or ('Bothell' in campuses)
            data['tacoma'] = data['tacoma'] or ('Tacoma' in campuses)

    if is_employee(request):
        # determine employee primary campus based on their mailstop
        try:
            employee_campus = get_employee_campus(request)
            data['official_seattle'] = ('Seattle' == employee_campus)
            data['official_bothell'] = ('Bothell' == employee_campus)
            data['official_tacoma'] = ('Tacoma' == employee_campus)
        except IndeterminateCampusException:
            pass

    request.myuw_user_affiliations = data
    return data


def get_is_hxt_viewer(request):
    is_fy_stud = in_fyp_group(request)
    is_aut_xfer = in_au_xfer_group(request)
    is_win_xfer = in_wi_xfer_group(request)
    is_sea_stud = is_seattle_student(request)
    is_undergrad = is_undergrad_student(request)
    # MUWM-4798
    is_viewer = in_hxtoolkit_group(request) or is_sea_stud and is_undergrad
    return (is_aut_xfer, is_fy_stud, is_win_xfer, is_sea_stud,
            is_undergrad, is_viewer)
