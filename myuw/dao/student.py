"""
This module will provide a method to retrieve all user majors, class standings
and minors along with current and rollup variables to facilitate
determinations about user context in the case that a user is not
enrolled for the current quarter
"""
from myuw.dao.enrollment import enrollment_search
from uw_sws.term import get_current_term


def get_student_status(request):
    """
    This will return a dictionary with the student status over time alongside
    various rollup variables
    :param request:
    :return: dict
    """
    enrollments = enrollment_search(request)
    if not hasattr(request, "student_status"):
        request.student_status = _process_fields(enrollments,
                                                 ['majors', 'minors',
                                                  'class_level'])

    return request.student_status


def get_majors(request):
    """
    Returns a dictionary with a dict of majors by terms in the 'majors'
    attribute, and a 'current' and 'rollup' major field
    :param request
    :return: dict
    """
    return get_student_status(request)['majors']


def get_rollup_and_future_majors(majors):
    return _get_rollup_and_future(majors['majors'], majors['rollup'])


def get_minors(request):
    """
    Returns a dictionary with a dict of majors by terms in the 'majors'
    attribute, and a 'current' and 'rollup' major field
    :param request
    :return: dict
    """
    return get_student_status(request)['minors']


def get_rollup_and_future_minors(minors):
    return _get_rollup_and_future(minors['minors'], minors['rollup'])


def get_class_levels(request):
    """
    Returns a dictionary with a dict of majors by terms in the majors
    attribute, and a 'current' and 'rollup' major field
    :param request
    :return: dict
    """
    return get_student_status(request)['class_level']


def _process_fields(enrollments, attributes):
    if len(attributes) == 0:
        return {}

    status = {}
    for attribute in attributes:
        status[attribute] = {}

    current_term = get_current_term()

    if current_term in enrollments:
        for attribute in attributes:
            status[attribute]['current'] = getattr(enrollments[current_term],
                                                attribute)

    for attribute in attributes:
        status[attribute][attribute] = {term: getattr(enrollments[term],
                                                   attribute)
                                     for term in enrollments}

    if 'current' not in status[attributes[0]]:
        sorted_terms = sorted(enrollments.keys())

        has_future_entry = False

        for term in sorted_terms:
            if term > current_term:
                for attribute in attributes:
                    status[attribute]['rollup'] = getattr(enrollments[term],
                                                       attribute)
                has_future_entry = True
                break

        recent_term = sorted_terms[0]

        if not has_future_entry:
            for term in sorted_terms:
                if term > recent_term:
                    recent_term = term

            for attribute in attributes:
                status[attribute]['rollup'] = getattr(enrollments[recent_term],
                                                   attribute)
    else:
        for attribute in attributes:
            status[attribute]['rollup'] = status[attribute]['current']

    return status


def _get_rollup_and_future(obj, rollup):
    objects = []
    current_term = get_current_term()

    for term in obj.keys():
        list_value = obj[term]
        for item in list_value:
            if term > current_term and item not in objects:
                objects.append(item)

    for item in rollup:
        if item not in objects:
            objects.append(item)

    return objects
