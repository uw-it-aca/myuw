"""
This module encapsulates the interactions with the uw_sws.person,
provides student record information of the current user
"""

from uw_sws.person import get_person_by_regid
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.enrollment import (get_current_quarter_enrollment,
                                 get_main_campus,
                                 get_all_enrollments,
                                 get_majors_for_terms,
                                 get_minors_for_terms)
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
    If the user is a student, returns the JSON response for that user's profile
    """
    regid = get_regid_of_current_user()
    profile = get_person_by_regid(regid)

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

    try:
        enrollments = get_all_enrollments()
    except Exception as ex:
        print ex
        logger.error(
            "%s get_academic_info: %s" %
            (netid, ex))
        return

    terms = get_current_and_next_quarters(request, 4)

    if terms[0] in enrollments:
        enrollment = enrollments[terms[0]]
        response['class_level'] = enrollment.class_level

    response['term_majors'] = get_majors_for_terms(terms, enrollments)
    response['has_pending_major'] = False

    for major in response['term_majors']:
        if not major['same_as_previous']:
            response['has_pending_major'] = True

    response['term_minors'] = get_minors_for_terms(terms, enrollments)
    response['has_pending_minor'] = False

    for minor in response['term_minors']:
        if not minor['same_as_previous']:
            response['has_pending_minor'] = True
