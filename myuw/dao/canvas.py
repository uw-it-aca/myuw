import logging
from restclients.canvas.enrollments import Enrollments
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.exceptions import CanvasNonSWSException
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time
import re


logger = logging.getLogger(__name__)


def get_canvas_active_enrollments():
    return _get_canvas_enrollment_dict_for_regid(
        get_regid_of_current_user())


def _get_canvas_enrollment_dict_for_regid(regid):
    return _enrollments_dict_by_sws_label(
        _get_canvas_active_enrollments_for_regid(regid))


def _get_canvas_active_enrollments_for_regid(regid):
    timer = Timer()
    try:
        return Enrollments().get_enrollments_for_regid(
            regid,
            {'type': ['StudentEnrollment'],
             'state': ['active']},
            include_courses=False)
    finally:
        pass
        log_resp_time(logger,
                      'get_canvas_active_enrollments',
                      timer)


def _enrollments_dict_by_sws_label(enrollments):
    """
    Returns active canvas enrollments for the current user.
    Raises: DataFailureException
    """
    enrollments_dict = {}
    for enrollment in enrollments:
        try:
            label = _sws_label_from_sis_id(enrollment.sis_section_id)
            enrollments_dict[label] = enrollment
        except CanvasNonSWSException:
            pass

    return enrollments_dict


def _sws_label_from_sis_id(sis_id):
    re_sis_id = re.compile(
        "^\d{4}-"                                  # year
        "(?:winter|spring|summer|autumn)-"         # quarter
        "[\w& ]+-"                                 # curriculum
        "\d{3}-"                                   # course number
        "[A-Z](?:[A-Z0-9]|--|-[A-F0-9]{32}--)?$",  # section id|regid
        re.VERBOSE)

    if not (sis_id and re_sis_id.match(sis_id)):
        raise CanvasNonSWSException("Non-academic SIS Id: %s" % sis_id)

    return "%s,%s,%s,%s/%s" % tuple(sis_id.strip('-').split('-'))


def canvas_prefetch():
    return [get_canvas_active_enrollments]
