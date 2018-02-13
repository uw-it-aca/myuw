"""
This module will provide a
"""
from uw_sws.enrollment import enrollment_search_by_regid


def get_student_status(regid):
    """
    This will return a dictionary with the student status over time alongside
    various rollup variables
    :param regid:
    :return: dict
    """
    enrollments = enrollment_search_by_regid(regid)

    return {
        'majors': _get_majors(regid, enrollments),
        'class_standing': _get_class_standings(regid, enrollments)
    }


def get_majors(regid):
    """
    Returns a dictionary with a dict of majors by terms in the 'majors'
    attribute, and a 'current' and 'rollup' major field
    :param regid
    :return: dict
    """
    pass


def _get_majors(regid, enrollments):
    pass


def get_class_standings(regid):
    """
    Returns a dictionary with a dict of majors by terms in the majors
    attribute, and a 'current' and 'rollup' major field
    :param regid
    :return: dict
    """
    pass


def _get_class_standings(regid, enrollments):
    pass


