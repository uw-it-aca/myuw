"""
This module provides affiliations of the current user
"""

import logging
from myuw_mobile.logger.logback import log_info
from myuw_mobile.dao.schedule import get_current_quarter_schedule
from myuw_mobile.dao.gws import is_grad_student, is_undergrad_student
from myuw_mobile.dao.gws import is_pce_student, is_student_employee
from myuw_mobile.dao.gws import is_seattle_student, is_bothell_student
from myuw_mobile.dao.gws import is_tacoma_student


logger = logging.getLogger(__name__)


def get_all_affiliations():
    """
    return a dictionary of affiliation indicators.
    ["grad"]: True if the user is currently an UW graduate student.
    ["undergrad"]: True if the user is currently an UW undergraduate student.
    ["pce"]: True if the user is currently an UW PCE student.
    ["stud_employee"]: True if the user is currently a student employee.
    ["seattle"]: True if the user is an UW Seattle student
                 in the current quarter.
    ["bothell"]: True if the user is an UW Bothell student
                 in the current quarter.             
    ["tacoma"]: True if the user is an UW Tacoma student
                in the current quarter.
    """
    enrolled_campuses = get_current_quarter_course_campuses()
    data = {"grad": is_grad_student(),
            "undergrad": is_undergrad_student(),
            "pce": is_pce_student(),
            "stud_employee": is_student_employee(),
            "seattle": enrolled_campuses["seattle"] or is_seattle_student(),
            "bothell": enrolled_campuses["bothell"] or is_bothell_student(),
            "tacoma": enrolled_campuses["tacoma"] or is_tacoma_student
            }
    # Note:
    #    As the UW Affiliation group (gws) only knows about one campus,
    #    we use registered sections in the current quarter
    #    to determine the campuses.
    log_info(logger, data)
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
                "tacoma": False}

    if schedule is not None and len(schedule.sections) > 0:
        for section in schedule.sections:
            if section.course_campus == "Seattle":
                campuses["seattle"]=True
            elif section.course_campus == "Bothell":
                campuses["bothell"]=True
            elif section.course_campus == "Tacoma":
                campuses["tacoma"]=True
            else:
                pass
    return campuses


def get_current_quarter_course_campuses():
    """
    Returns a dictionary indicating the campuses that the student
    has enrolled in the current quarter.
    """
    return _get_campuses_by_schedule(get_current_quarter_schedule())

