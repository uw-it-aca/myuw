"""
This class encapsulates the interactions with
the SWS Enrollment resource.
"""

import logging
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception, log_info
from datetime import date
from uw_sws.enrollment import enrollment_search_by_regid
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


def get_all_enrollments():
    """
    :return: the dictionary of {Term: Enrollment}
    """
    regid = get_regid_of_current_user()
    return enrollment_search_by_regid(regid)


def get_current_quarter_enrollment(request):
    """
    :return: an Enrollment object
    """
    if hasattr(request, 'my_curq_enrollment'):
        return request.my_curq_enrollment
    enrollment = get_enrollment_for_term(get_current_quarter(request))
    request.my_curq_enrollment = enrollment
    return enrollment


def get_enrollment_for_term(term):
    """
    :return: an Enrollment object
    """
    return get_all_enrollments().get(term)


def get_enrollments_of_terms(term_list):
    """
    :return: the dictionary of {Term: Enrollment} of the given terms
    """
    result_dict = get_all_enrollments()
    selected_dict = {}
    for term in term_list:
        if term in result_dict:
            selected_dict[term] = result_dict[term]
    return selected_dict


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


def _get_degrees_for_terms(terms, enrollments, accessor):
    """
    Takes in a list of terms and a dictionary of terms to enrollments (returned
    by get_all_enrollments), and returns a list of either majors or minors
    and their terms, depending upon which accessor is used, 'majors' or
    'minors'
    """
    degrees = []
    previous = None

    for term in terms:
        if term in enrollments:
            previous = getattr(enrollments[term], accessor)
            break

    for term in terms:
        if (term in enrollments and
                len(getattr(enrollments[term], accessor)) > 0):
            enrollment = enrollments[term]
            entry = {}
            entry['quarter'] = term.quarter
            entry['year'] = term.year

            term_degrees = getattr(enrollments[term], accessor)
            entry[accessor] = []

            entry['same_as_previous'] = _compare_degrees(previous,
                                                         term_degrees)

            for degree in term_degrees:
                entry[accessor].append(degree.json_data())

            degrees.append(entry)
            previous = term_degrees

    return degrees


def get_majors_for_terms(terms, enrollments):
    """
    Takes in a list of terms and a dictionary of terms to enrollments (returned
    by get_all_enrollments), and returns a list of majors and their terms
    """
    return _get_degrees_for_terms(terms, enrollments, 'majors')


def get_minors_for_terms(terms, enrollments):
    """
    Takes in a list of terms and a dictionary of terms to enrollments (returned
    by get_all_enrollments), and returns a list of minors and their terms
    """
    return _get_degrees_for_terms(terms, enrollments, 'minors')


def _compare_degrees(first, second):
    """
    Takes in two lists of degrees (either major or minors) and checks to see
    if they are the same. Returns True if so, False if they are different
    """
    if len(first) != len(second):
        return False

    degrees = {}
    for entry in first:
        degrees[entry.full_name] = entry

    for entry in second:
        if entry.full_name not in degrees:
            return False
        else:
            del degrees[entry.full_name]

    return True


def enrollment_prefetch():
    def _method(request):
        return get_all_enrollments()
    return [_method]


def get_code_for_class_level(class_name):
    if class_name in CLASS_CODES:
        return CLASS_CODES[class_name]
    return DEFAULT_CLASS_CODE
