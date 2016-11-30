"""
This module provides affiliations of the current user
"""

import logging
import traceback
from django.conf import settings
from myuw.logger.logback import log_info, log_exception
from myuw.dao.schedule import get_current_quarter_schedule
from myuw.dao.pws import get_netid_of_current_user
from myuw.dao.gws import is_grad_student, is_student,\
    is_current_graduate_student, is_undergrad_student,\
    is_pce_student, is_student_employee, is_employee, is_faculty,\
    is_seattle_student, is_bothell_student, is_tacoma_student,\
    is_staff_employee
from myuw.dao.enrollment import get_main_campus
from myuw.dao.user import is_fyp_thrive_viewer


logger = logging.getLogger(__name__)


def get_all_affiliations(request):
    """
    return a dictionary of affiliation indicators.
    ["student"]: True if the user is currently an UW student.
    ["grad"]: True if the user is currently an UW graduate student.
    ["undergrad"]: True if the user is currently an UW undergraduate student.
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
    """

    if hasattr(request, 'myuw_user_affiliations'):
        return request.myuw_user_affiliations

    enrolled_campuses = get_current_quarter_course_campuses(request)
    is_fyp = False
    try:
        is_fyp = is_thrive_viewer()
    except Exception:
        # This fails in unit tests w/o userservice
        pass

    data = {"grad": is_grad_student(),
            "undergrad": is_undergrad_student(),
            "student": is_student(),
            "pce": is_pce_student(),
            "stud_employee": is_student_employee(),
            "employee": is_employee(),
            "fyp": is_fyp,
            "faculty": is_faculty(),
            "seattle": enrolled_campuses["seattle"] or is_seattle_student(),
            "bothell": enrolled_campuses["bothell"] or is_bothell_student(),
            "tacoma": enrolled_campuses["tacoma"] or is_tacoma_student(),
            }
    # add 'official' campus info
    official_campuses = _get_official_campuses(get_main_campus(request))
    data = dict(data.items() + official_campuses.items())
    # Note:
    #    As the UW Affiliation group (gws) only knows about one campus,
    #    we use registered sections in the current quarter
    #    to determine the campuses.
    log_info(logger, data)
    request.myuw_user_affiliations = data
    return data


def is_thrive_viewer():
    return is_fyp_thrive_viewer(get_netid_of_current_user())


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
                "tacoma": False}

    if schedule is not None and len(schedule.sections) > 0:
        for section in schedule.sections:
            if section.course_campus == "Seattle":
                campuses["seattle"] = True
            elif section.course_campus == "Bothell":
                campuses["bothell"] = True
            elif section.course_campus == "Tacoma":
                campuses["tacoma"] = True
            else:
                pass
    return campuses


def _get_official_campuses(campuses):
    official_campuses = {'official_seattle': False,
                         'official_bothell': False,
                         'official_tacoma': False}
    for campus in campuses:
        if campus == "Seattle":
            official_campuses['official_seattle'] = True
        if campus == "Tacoma":
            official_campuses['official_tacoma'] = True
        if campus == "Bothell":
            official_campuses['official_bothell'] = True
    return official_campuses


def get_current_quarter_course_campuses(request):
    """
    Returns a dictionary indicating the campuses that the student
    has enrolled in the current quarter.
    """
    try:
        current_quarter_sche = get_current_quarter_schedule(request)
    except Exception as ex:
        log_exception(logger,
                      'get_current_quarter_course_campuses',
                      traceback.format_exc())
        current_quarter_sche = None
    return _get_campuses_by_schedule(current_quarter_sche)


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
