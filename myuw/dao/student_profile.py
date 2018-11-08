"""
This module encapsulates the interactions with the uw_sws.person,
provides student record information of the current user
"""

import logging
from uw_sws.person import get_person_by_regid
from myuw.dao import get_netid_of_current_user
from myuw.dao.gws import is_grad_student
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.enrollment import get_main_campus, get_enrollments_of_terms
from myuw.dao.term import get_current_and_next_quarters


logger = logging.getLogger(__name__)


def sws_person_prefetch():
    def _method(request):
        return get_profile_of_current_user(request)
    return [_method]


def get_profile_of_current_user(request):
    """
    Return uw_sws.models.SwsPerson object
    """
    regid = get_regid_of_current_user(request)
    return get_person_by_regid(regid)


def get_applicant_profile(request):
    return get_profile_of_current_user(request).json_data()


def get_student_profile(request):
    """
    Returns the JSON response for a student's profile
    """
    profile = get_applicant_profile(request)

    response = profile
    response['is_student'] = True
    response['is_grad_student'] = is_grad_student(request)

    campuses = get_main_campus(request)
    if 'Seattle' in campuses:
        response['campus'] = 'Seattle'
    elif 'Tacoma' in campuses:
        response['campus'] = 'Tacoma'
    elif 'Bothell' in campuses:
        response['campus'] = 'Bothell'

    get_academic_info(request, response)
    return response


def get_cur_future_enrollments(request):
    try:
        terms = get_current_and_next_quarters(request, 4)
        return terms, get_enrollments_of_terms(request, terms)
    except Exception as ex:
        logger.error("{} get_enrollments: {}".format(
            get_netid_of_current_user(request), str(ex)))
        return None


def get_academic_info(request, response):
    """
    Iterates through the student enrollments and populates the profile
    fields based upon data available
    """
    terms, enrollments = get_cur_future_enrollments(request)

    if terms[0] in enrollments:
        enrollment = enrollments[terms[0]]
        response['class_level'] = enrollment.class_level

    response['term_majors'] = _get_degrees_for_terms(terms, enrollments,
                                                     "majors")
    response['has_pending_major'] = False

    for major in response['term_majors']:
        if major['degrees_modified']:
            response['has_pending_major'] = True

    response['term_minors'] = _get_degrees_for_terms(terms, enrollments,
                                                     "minors")

    for minor in response['term_minors']:
        if len(minor['minors']) > 0:
            response['has_minors'] = True

    response['has_pending_minor'] = False

    for minor in response['term_minors']:
        if minor['degrees_modified']:
            response['has_pending_minor'] = True


def _get_degrees_for_terms(terms, enrollments, accessor):
    """
    Takes in a list of terms and a dictionary of terms to enrollments, and
    returns a list of either majors or minors and their terms, depending upon
    which accessor is used, 'majors' or 'minors'
    """
    degrees = []
    previous = None

    for term in terms:
        if term in enrollments:
            previous = getattr(enrollments[term], accessor)
            break

    for term in terms:
        if term in enrollments:
            entry = {}
            entry['quarter'] = term.quarter
            entry['year'] = term.year

            term_degrees = getattr(enrollments[term], accessor)
            entry[accessor] = []

            entry['degrees_modified'] = _degree_has_changed(previous,
                                                            term_degrees)

            entry['has_only_dropped'] = _has_only_dropped_degrees(
                                                             previous,
                                                             term_degrees)
            for degree in term_degrees:
                entry[accessor].append(degree.json_data())

            degrees.append(entry)
            previous = term_degrees

    return degrees


def _degree_has_changed(first, second):
    """
    Takes in two lists of degrees (either major or minors) and checks to see
    if they are the same. Returns False if so, True if they are different
    """
    return len(set(first) ^ set(second)) != 0


def _has_only_dropped_degrees(first, second):
    """
    Returns True if the user has only dropped degrees from first, and False
    if there have been either no degrees dropped or one added.
    """
    has_dropped = len(set(first) - set(second)) > 0
    has_added = len(set(second) - set(first)) > 0
    return has_dropped and not has_added
