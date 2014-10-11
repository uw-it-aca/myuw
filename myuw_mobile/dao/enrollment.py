"""
This class encapsulates the interactions with 
the SWS Enrollment resource.
"""

import logging
import traceback
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception, log_info
from myuw_mobile.dao.pws import get_regid_of_current_user
from restclients.sws.enrollment import get_enrollment_by_regid_and_term
from myuw_mobile.dao.term import get_current_quarter
logger = logging.getLogger(__name__)


def get_current_quarter_enrollment():
    regid = get_regid_of_current_user()

    timer = Timer()
    id = "%s %s" % ('get enrollment by regid', regid)
    try:
        return get_enrollment_by_regid_and_term(regid, get_current_quarter())
    except Exception:
        log_exception(logger,
                      id,
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      id,
                      timer)
    return None


def get_main_campus():
    enrollment = get_current_quarter_enrollment()
    if enrollment is None:
        return None
    campuses = []
    for major in enrollment.majors:
        campuses.append(major.campus)
        return campuses


