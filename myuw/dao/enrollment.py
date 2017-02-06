"""
This class encapsulates the interactions with
the SWS Enrollment resource.
"""

import logging
from restclients.sws.enrollment import get_enrollment_by_regid_and_term
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_current_quarter


logger = logging.getLogger(__name__)


def get_current_quarter_enrollment(request):
    regid = get_regid_of_current_user()
    return get_enrollment_by_regid_and_term(regid,
                                            get_current_quarter(request))


def get_main_campus(request):
    campuses = []
    try:
        enrollment = get_current_quarter_enrollment(request)
    except Exception as ex:
        logger.error("get_current_quarter_enrollment: %s" % ex)
        return campuses
    for major in enrollment.majors:
        campuses.append(major.campus)
    return campuses


def enrollment_prefetch():
    def _method(request):
        return get_current_quarter_enrollment(request)

    return [_method]
