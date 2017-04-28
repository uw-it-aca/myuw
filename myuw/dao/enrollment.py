"""
This class encapsulates the interactions with
the SWS Enrollment resource.
"""

import logging
from uw_sws.enrollment import get_enrollment_by_regid_and_term
from uw_sws.section import validate_section_label
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_current_quarter, get_comparison_datetime
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


def find_enrolled_independent_start_section(request, section_label):
    validate_section_label(section_label)
    enrollment = get_current_quarter_enrollment(request)
    for i_sect in enrollment.independent_start_sections:
        if i_sect.section_ref.section_label() == section_label:
            ended = get_comparison_datetime(request) > i_sect.end_date
            return i_sect, ended


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


def enrollment_prefetch():
    def _method(request):
        return get_current_quarter_enrollment(request)

    return [_method]


def get_code_for_class_level(class_name):
    if class_name in CLASS_CODES:
        return CLASS_CODES[class_name]

    return DEFAULT_CLASS_CODE
