import logging
from restclients.canvas.enrollments import Enrollments
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.exceptions import CanavsNonSWSException
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time
import re


logger = logging.getLogger(__name__)


def get_canvas_active_enrollments():
    """
    Returns active canvas enrollments for the current user.
    Raises: DataFailureException
    """
    enrollments = {}
    for enrollment in _get_canvas_active_enrollments():
        try:
            label = _sws_label_from_sis_id(enrollment.sis_section_id)
            enrollments[label] = enrollment
        except CanavsNonSWSException:
            pass

    return enrollments


def get_canvas_course_url_from_enrollment(enrollment):
    match = re.match(r'^(https://[^/]+/courses/\d+)(/.*)?$',
                     enrollment.html_url)
    if match:
        return match.group(1)

    return None


def _get_canvas_active_enrollments():
    timer = Timer()
    try:
        return Enrollments().get_enrollments_for_regid(
            get_regid_of_current_user(),
            {'type': ['StudentEnrollment'],
             'state': ['active']},
            include_course=False)
    finally:
        pass
        log_resp_time(logger,
                      'get_canvas_active_enrollments',
                      timer)


def _sws_label_from_sis_id(sis_id):
    re_sis_id = re.compile(
        "^\d{4}-"                                  # year
        "(?:winter|spring|summer|autumn)-"         # quarter
        "[\w& ]+-"                                 # curriculum
        "\d{3}-"                                   # course number
        "[A-Z](?:[A-Z0-9]|--|-[A-F0-9]{32}--)?$",  # section id|regid
        re.VERBOSE)

    if not (sis_id and re_sis_id.match(sis_id)):
        raise CanavsNonSWSException("Non-academic SIS Id: %s" % sis_id)

    return "%s,%s,%s,%s/%s" % tuple(sis_id.strip('-').split('-'))


def canvas_prefetch():
    return [get_canvas_active_enrollments]
