"""
This class encapsulates the interactions with
the SWS Enrollment resource.
"""

import logging
from uw_sws.enrollment import (get_enrollment_by_regid_and_term,
                               enrollment_search_by_regid)
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception, log_info
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_current_quarter
from restclients_core.exceptions import DataFailureException
from myuw.dao.exceptions import IndeterminateCampusException


CLASS_CODES = {
    "FRESHMAN": 1,
    "SOPHOMORE": 2,
    "JUNIOR": 3,
    "SENIOR": 4,
    "GRADUATE": 5,
}


DEFAULT_CLASS_CODE = 6


logger = logging.getLogger(__name__)


def get_current_quarter_enrollment(request):
    regid = get_regid_of_current_user()
    return get_enrollment_by_regid_and_term(regid,
                                            get_current_quarter(request))


def get_all_enrollments():
    regid = get_regid_of_current_user()

    timer = Timer()
    id = "%s %s" % ('get all enrollment by regid', regid)
    try:
        return enrollment_search_by_regid(regid)
    finally:
        log_resp_time(logger,
                      id,
                      timer)


def get_main_campus(request):
    campuses = []
    try:
        enrollment = get_current_quarter_enrollment(request)
        for major in enrollment.majors:
            campuses.append(major.campus)
    except DataFailureException as ex:
        logger.error("get_current_quarter_enrollment: %s" % ex)
        raise IndeterminateCampusException()
    except Exception as ex:
        logger.error("get_current_quarter_enrollment: %s" % ex)
        pass

    return campuses


def get_majors_for_terms(terms, enrollments):
    """
    Takes in a list of terms and a dictionary of terms to enrollments (returned
    by get_all_enrollments), and returns a list of majors and their terms
    """

    majors = []
    previous = None

    for term in terms:
        if (term in enrollments and len(enrollments[term].majors) > 0):
            enrollment = enrollments[term]
            major_entry = {}
            major_entry['quarter'] = term.quarter
            major_entry['year'] = term.year

            major_entry['majors'] = []

            for major in enrollments[term].majors:
                major_entry['majors'].append(major.json_data())
                if previous is not None:
                    major_entry['same_as_previous'] = _compare_degrees(previous, enrollments[term].majors)
                else:
                    major_entry['same_as_previous'] = True

            majors.append(major_entry)
            previous = enrollments[term].majors

    return majors


def get_minors_for_terms(terms, enrollments):
    """
    Takes in a list of terms and a dictionary of terms to enrollments (returned
    by get_all_enrollments), and returns a list of minors and their terms
    """

    minors = []
    previous = None

    for term in terms:
        previous = enrollments[term].minors
        if term in enrollments and len(enrollments[term].minors) > 0:
            enrollment = enrollments[term]
            minor_entry = {}
            minor_entry['quarter'] = term.quarter
            minor_entry['year'] = term.year

            minor_entry['minors'] = []

            for minor in enrollments[term].minors:
                minor_entry['minors'].append(minor.json_data())
                if previous is not None:
                    minor_entry['same_as_previous'] = _compare_degrees(previous, enrollments[term].minors)
                else:
                    minor_entry['same_as_previous'] = True

            minors.append(minor_entry)
            previous = enrollments[term].minors

    return minors


def _compare_degrees(first, second):
    """
    Takes in two lists of degrees (either major or minors) and checks to see
    if they are the same. Returns True if so, False if they are different
    """
    if len(first) != len(second):
        return False

    for entry in first:
        entry_in_second = False
        for obj in second:
            if obj.full_name == entry.full_name:
                entry_in_second = True
        if not entry_in_second:
            return False

    return True


def enrollment_prefetch():
    def _method(request):
        return get_current_quarter_enrollment(request)

    return [_method]


def get_code_for_class_level(class_name):
    if class_name in CLASS_CODES:
        return CLASS_CODES[class_name]

    return DEFAULT_CLASS_CODE
