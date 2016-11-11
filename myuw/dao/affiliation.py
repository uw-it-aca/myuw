"""
This module provides affiliations of the current user
"""

import os
import json
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
from myuw.models import UserMigrationPreference


THRIVE = "thrive"
OPTIN = "optin"
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


def get_fast_affiliations(request):
    """
    A list of affiliations that can be done in a single lookup.
    ["student"]: True if the user is currently an UW student.
    ["grad"]: True if the user is currently an UW graduate student.
    ["undergrad"]: True if the user is currently an UW undergraduate student.
    ["pce"]: True if the user is currently an UW PCE student.
    ["employee"]: True if the user is currently a uw employee.
    ["stud_employee"]: True if the user is currently a student employee.
    ["faculty"]: True if the user is currently faculty.

    """
    if hasattr(request, 'myuw_fast_user_affiliations'):
        return request.myuw_fast_user_affiliations

    is_fyp = False
    try:
        is_fyp = is_thrive_viewer()
    except Exception:
        # This fails in unit tests w/o userservice
        pass

    data = {"grad": request_cached_is_grad_student(request),
            "undergrad": request_cached_is_undergrad(request),
            "student": request_cached_is_student(request),
            "pce": request_cached_is_pce_student(request),
            "stud_employee": request_cached_is_student_employee(request),
            "employee": request_cached_is_employee(request),
            "fyp": is_fyp,
            "faculty": request_cached_is_faculty(request),
            }

    request.myuw_fast_user_affiliations = data
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


def is_oldmyuw_user():
    if has_legacy_preference():
        return True
    if is_optin_user():
        return False
    if is_staff_employee():
        return True
    if is_faculty():
        return True
    if is_current_graduate_student():
        return True
    if is_undergrad_student():
        return False
    return True


def has_legacy_preference():
    username = get_netid_of_current_user()

    try:
        saved = UserMigrationPreference.objects.get(username=username)
        if saved.use_legacy_site:
            return True
    except UserMigrationPreference.DoesNotExist:
        return False
    return False


def is_optin_user():
    return _is_user_in_list(
        get_netid_of_current_user(), OPTIN)


def is_thrive_viewer():
    return _is_user_in_list(
        get_netid_of_current_user(), THRIVE)


def _is_user_in_list(username, user_type):
    if THRIVE == user_type:
        file_path = getattr(settings, "MYUW_MANDATORY_SWITCH_PATH", None)
        if not file_path:
            current_dir = os.path.dirname(os.path.realpath(__file__))

            file_path = os.path.abspath(os.path.join(current_dir,
                                                     "..", "data",
                                                     "thrive-viewer-list.txt"))

    else:
        file_path = getattr(settings, "MYUW_OPTIN_SWITCH_PATH", None)
        if not file_path:
            current_dir = os.path.dirname(os.path.realpath(__file__))

            file_path = os.path.abspath(os.path.join(current_dir,
                                                     "..", "data",
                                                     "optin-list.txt"))

    with open(file_path) as data_source:
        for line in data_source:
            if line.rstrip() == username:
                return True

    return False


def _build_cache_method(name, method):
    name = "myuw_cache_%s" % name

    def generated(request):
        if hasattr(request, name):
            print "Hey, cached: ", name
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


request_cached_is_faculty = _build_cache_method("faculty",
                                                is_faculty)


def index_affiliation_prefetch():
    return [request_cached_is_grad_student,
            request_cached_is_undergrad,
            request_cached_is_student,
            request_cached_is_pce_student,
            request_cached_is_student_employee,
            request_cached_is_employee,
            request_cached_is_faculty,
            ]
