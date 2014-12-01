from restclients.canvas.enrollments import Enrollments as CanvasEnrollments
from myuw_mobile.dao.pws import get_regid_of_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception
import logging
import traceback


logger = logging.getLogger(__name__)


def get_canvas_enrolled_courses():
    """
    Returns calendar information for the current term.
    """
    timer = Timer()
    try:
        regid = get_regid_of_current_user()
        return _indexed_by_course_id(
            CanvasEnrollments().get_enrollments_for_regid(
                regid,
                {'state': "active",
                 'as_user': CanvasEnrollments().sis_user_id(regid)})
        )
    except AttributeError:
        # If course is not in canvas, skip
        pass
    except Exception as ex:
        log_exception(logger,
                      'get_canvas_enrolled_courses',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      'get_canvas_enrolled_courses',
                      timer)
    return []


def _indexed_by_course_id(enrollments):
    """
    return a dictionary of SWS course id to enrollment.
    """
    canvas_data_by_course_id = {}
    if enrollments and len(enrollments) > 1:
        for enrollment in enrollments:
            canvas_data_by_course_id[enrollment.sws_course_id()] = enrollment
    return canvas_data_by_course_id
