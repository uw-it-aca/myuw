"""
This module encapsulates the interactions with the uw_sws.person,
provides student record information of the current user
"""

from uw_sws.person import get_person_by_regid
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.enrollment import (get_current_quarter_enrollment,
                                 get_main_campus,
                                 get_enrollments_of_terms)
from myuw.dao.term import (get_current_quarter,
                           get_next_quarter,
                           get_current_and_next_quarters)
from myuw.dao.gws import is_grad_student


def get_profile_of_current_user():
    """
    Return uw_sws.models.SwsPerson object
    """
    regid = get_regid_of_current_user()
    return get_person_by_regid(regid)


def get_student_profile(request):
    """
    Returns the JSON response for a student's profile
    """
    profile = get_profile_of_current_user()

    response = profile.json_data()
    response['is_student'] = True
    response['is_grad_student'] = is_grad_student()

    campuses = get_main_campus(request)
    if 'Seattle' in campuses:
        response['campus'] = 'Seattle'
    elif 'Tacoma' in campuses:
        response['campus'] = 'Tacoma'
    elif 'Bothell' in campuses:
        response['campus'] = 'Bothell'

    get_academic_info(request, response)

    return response


def get_academic_info(request, response):
    """
    Iterates through the student enrollments and populates the profile
    fields based upon data available
    """

    terms = get_current_and_next_quarters(request, 4)

    try:
        enrollments = get_enrollments_of_terms(terms)
    except Exception as ex:
        logger.error(
            "%s get_academic_info: %s" %
            (netid, ex))
        return

    if terms[0] in enrollments:
        enrollment = enrollments[terms[0]]
        response['class_level'] = enrollment.class_level

    response['term_majors'] = _get_majors_for_terms(terms, enrollments)
    response['has_pending_major'] = False

    for major in response['term_majors']:
        if not major['same_as_previous']:
            response['has_pending_major'] = True

    response['term_minors'] = _get_minors_for_terms(terms, enrollments)
    response['has_pending_minor'] = False

    if (len(response['term_minors']) > 1 and
            len(response['term_minors'][0]['minors']) > 0):
        response['has_minors'] = True

    for minor in response['term_minors']:
        if not minor['same_as_previous']:
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

                entry['same_as_previous'] = _compare_degrees(previous,
                                                             term_degrees)

                entry['has_only_dropped'] = _has_only_dropped_degrees(
                                                                 previous,
                                                                 term_degrees)
                for degree in term_degrees:
                    entry[accessor].append(degree.json_data())

                degrees.append(entry)
                previous = term_degrees

    return degrees


def _get_majors_for_terms(terms, enrollments):
    """
    Takes in a list of terms and a dictionary of terms to enrollments,
    and returns a list of majors and their terms
    """
    return _get_degrees_for_terms(terms, enrollments, 'majors')


def _get_minors_for_terms(terms, enrollments):
    """
    Takes in a list of terms and a dictionary of terms to enrollments, and
    returns a list of minors and their terms
    """
    return _get_degrees_for_terms(terms, enrollments, 'minors')


def _compare_degrees(first, second):
    """
    Takes in two lists of degrees (either major or minors) and checks to see
    if they are the same. Returns True if so, False if they are different
    """
    return len(set(first) ^ set(second)) == 0


def _has_only_dropped_degrees(first, second):
    """
    Returns True if the user has only dropped degrees from first, and False
    if there have been either no degrees dropped or one added.
    """
    has_dropped = len(set(first) - set(second)) > 0
    has_added = len(set(second) - set(first)) > 0
    return (has_dropped and not has_added)
