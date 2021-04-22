# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the SWS Enrollment resource.
"""
import datetime
import logging
import traceback
from copy import deepcopy
from uw_sws.enrollment import (
    enrollment_search_by_regid, get_enrollment_history_by_regid)
from myuw.dao import log_err
from myuw.dao.term import (
    get_current_quarter, get_current_and_next_quarters,
    get_previous_number_quarters, get_comparison_date)
from restclients_core.exceptions import DataFailureException
from myuw.dao.pws import get_regid_of_current_user

CLASS_CODES = {
    "FRESHMAN": 1,
    "SOPHOMORE": 2,
    "JUNIOR": 3,
    "SENIOR": 4,
    "POST-BACCALAUREATE": 5,
    "NON_MATRIC": 6,
    "GRADUATE": 8
}
DEFAULT_CLASS_CODE = 9
logger = logging.getLogger(__name__)


def enrollment_search(request):
    if not hasattr(request, "academic_enrollments"):
        request.academic_enrollments = enrollment_search_by_regid(
            get_regid_of_current_user(request))
    return request.academic_enrollments


def enrollment_prefetch():
    def _method(request):
        return enrollment_search(request)
    return [_method]


def get_enrollment_for_term(request, term):
    """
    :return: an Enrollment object or None if no object exists
    """
    enrollments = enrollment_search(request)
    return enrollments.get(term)


def get_enrollments_of_terms(request, term_list):
    """
    :return: the dictionary of {Term: Enrollment} of the given terms
    """
    enrollments = enrollment_search(request)
    selected_dict = {}
    for term in term_list:
        if term in enrollments:
            selected_dict[term] = enrollments.get(term)
    return selected_dict


def get_current_quarter_enrollment(request):
    """
    :return: an Enrollment object
    """
    return get_enrollment_for_term(request,
                                   get_current_quarter(request))


def get_prev_enrollments_with_open_sections(request, num_of_prev_terms):
    """
    :return: the dictionary of {Term: Enrollment} of the given
    number of previous terms with unfinished sections
    """
    terms = get_previous_number_quarters(request, num_of_prev_terms)
    result_dict = get_enrollments_of_terms(request, terms)
    return remove_finished(request, result_dict)


def is_registered_current_quarter(request):
    try:
        enrollment = get_current_quarter_enrollment(request)
        return enrollment is not None and enrollment.is_registered
    except Exception:
        log_err(logger, "is_registered_current_quarter", traceback, request)
    return False


def get_main_campus(request):
    campuses = []
    try:
        result_dict = get_enrollments_of_terms(
            request, get_current_and_next_quarters(request, 2))

        for term in result_dict.keys():
            enrollment = result_dict.get(term)
            for major in enrollment.majors:
                if major.campus and major.campus not in campuses:
                    campuses.append(major.campus)
    except Exception:
        log_err(logger, "get_main_campus", traceback, request)
    return campuses


def get_class_level(request):
    """
    Return current term class level
    """
    enrollment = get_current_quarter_enrollment(request)
    if enrollment:
        return enrollment.class_level
    return None


def get_code_for_class_level(class_name):
    if class_name in CLASS_CODES:
        return CLASS_CODES[class_name]
    return DEFAULT_CLASS_CODE


def is_ended(request, end_date):
    """
    Return True only when end_date is a valid date and is in the past
    """
    now = get_comparison_date(request)
    return end_date and isinstance(end_date, datetime.date) and now > end_date


def remove_finished(request, result_dict):
    # keep the sections that aren't finished
    for prev_term in result_dict.keys():
        enrollment = result_dict.get(prev_term)
        if enrollment.has_unfinished_pce_course():
            unf_pce_sections = enrollment.unf_pce_courses
            for label in deepcopy(unf_pce_sections):
                section = unf_pce_sections[label]
                if is_ended(request, section.end_date):
                    del unf_pce_sections[label]
    return result_dict


def enrollment_history(request):
    """
    The underline uw_sws call is the same as enrollment_search
    :return: a chronological list of all the Enrollemnts ordered by Term
    """
    if not hasattr(request, "enrollment_history"):
        request.enrollment_history = get_enrollment_history_by_regid(
            get_regid_of_current_user(request))
    return request.enrollment_history
