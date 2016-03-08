import logging
from restclients.canvas.enrollments import Enrollments as CanvasEnrollments
from restclients.canvas.sections import Sections
from restclients.canvas.courses import Courses
from myuw.dao.pws import get_regid_of_current_user
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception


logger = logging.getLogger(__name__)


def get_canvas_enrolled_courses():
    """
    Returns calendar information for the current term.
    Raises: DataFailureException
    """
    timer = Timer()
    try:
        regid = get_regid_of_current_user()
        return get_indexed_data_for_regid(regid)
    except AttributeError:
        # If course is not in canvas, skip
        return []
    finally:
        log_resp_time(logger,
                      'get_canvas_enrolled_courses',
                      timer)


def get_indexed_data_for_regid(regid):
    return _indexed_by_course_id(
        CanvasEnrollments().get_enrollments_for_regid(
            regid,
            {'state': "active",
             'as_user': CanvasEnrollments().sis_user_id(regid)})
        )


def get_indexed_by_decrosslisted(by_primary, sws_sections):
    for section in sws_sections:
        base_id = section.section_label()
        alternate_id = None
        try:
            sis_id = section.canvas_section_sis_id()
            canvas_section = Sections().get_section_by_sis_id(sis_id)
            primary_course = Courses().get_course(canvas_section.course_id)
            alternate_id = primary_course.sws_course_id()
        except Exception as ex:
            # primary section doesn't have canvas_section_sis_id
            alternate_id = base_id

        if base_id not in by_primary:
            if alternate_id in by_primary:
                by_primary[base_id] = by_primary[alternate_id]
    return by_primary


def _indexed_by_course_id(enrollments):
    """
    return a dictionary of SWS course id to enrollment.
    """
    canvas_data_by_course_id = {}
    if enrollments and len(enrollments) > 1:
        for enrollment in enrollments:
            canvas_data_by_course_id[enrollment.sws_course_id()] = enrollment
    return canvas_data_by_course_id
