"""
This class encapsulates the interactions with
the SWS Enrollment resource.
"""

import logging
from datetime import date
from uw_sws.enrollment import enrollment_search_by_regid
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import (get_current_quarter,
                           get_prev_num_terms,
                           get_comparison_date)
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


def get_code_for_class_level(class_name):
    if class_name in CLASS_CODES:
        return CLASS_CODES[class_name]
    return DEFAULT_CLASS_CODE


def enrollment_prefetch():
    def _method(request):
        return get_all_enrollments()
    return [_method]


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
    return get_enrollment_of_aterm(get_current_quarter(request))


def get_enrollment_of_aterm(aterm):
    """
    :return: an Enrollment object
    """
    return get_all_enrollments().get(aterm)


def get_enrollments_of_terms(term_list):
    """
    :return: the dictionary of {Term: Enrollment} of the given terms
    """
    result_dict = get_all_enrollments()
    terms = result_dict.keys()
    for key in terms:
        if key not in term_list:
            del result_dict[key]
    return result_dict


def get_prev_enrollments_with_open_sections(request, num_of_prev_terms):
    """
    :return: the dictionary of {Term: Enrollment} of the given
    number of previous terms with unfinished sections
    """
    terms = get_prev_num_terms(request, num_of_prev_terms)
    result_dict = get_enrollments_of_terms(terms)

    # only keep the sections that aren't finished
    for prev_term in result_dict.keys():
        enrollment = result_dict.get(prev_term)
        if enrollment.has_off_term_course():
            off_term_sections = enrollment.off_term_sections
            section_labels = off_term_sections.keys()
            for label in section_labels:
                section = off_term_sections[label]
                if is_ended(request, section.end_date):
                    del off_term_sections[label]
    return result_dict


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


def is_ended(request, end_date):
    if len(str(end_date)) == 0:
        return False
    now = get_comparison_date(request)
    end_date = date(end_date.year,
                    end_date.month,
                    end_date.day)
    return now > end_date
