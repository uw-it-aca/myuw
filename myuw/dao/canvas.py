import logging
from restclients.canvas.enrollments import Enrollments
from restclients.canvas.courses import Courses
from restclients.exceptions import DataFailureException
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.exceptions import CanvasNonSWSException
import re


logger = logging.getLogger(__name__)


def get_canvas_active_enrollments():
    return _get_canvas_enrollment_dict_for_regid(
        get_regid_of_current_user())


def _get_canvas_enrollment_dict_for_regid(regid):
    return _enrollments_dict_by_sws_label(
        _get_canvas_active_enrollments_for_regid(regid))


def _get_canvas_active_enrollments_for_regid(regid):
    return Enrollments().get_enrollments_for_regid(
        regid,
        {'type': ['StudentEnrollment'],
         'state': ['active']},
        include_courses=False)


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

    return "%s,%s,%s,%s/%s" % tuple(sis_id.strip('-').split('-')[:5])


def get_canvas_course_from_section(sws_section):
    try:
        return Courses().get_course_by_sis_id(
            sws_section.canvas_course_sis_id())
    except DataFailureException as err:
        if err.status == 404:
            return None

        raise


def get_canvas_course_url(sws_section):
    canvas_course = get_canvas_course_from_section(sws_section)
    if canvas_course:
        return canvas_course.course_url


def canvas_course_is_available(canvas_id):
    try:
        course = Courses().get_course(canvas_id)
        return course.workflow_state.lower() in ['available', 'concluded']
    except DataFailureException as ex:
        if ex.status == 404:
            return False


def canvas_prefetch():
    return [get_canvas_active_enrollments]
