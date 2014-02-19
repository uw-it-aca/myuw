from restclients.canvas.enrollments import Enrollments as CanvasEnrollments
from myuw_mobile.dao.pws import Person
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception
import logging
import traceback


class Enrollments:
    def get_enrollments(self):
        """
        Returns calendar information for the current term.
        """
        timer = Timer()
        logger = logging.getLogger('myuw_mobile.dao.canvas.Enrollments')
        regid = Person().get_regid()
        try:
            return CanvasEnrollments().get_enrollments_for_regid(regid)
        except Exception as ex:
            log_exception(logger,
                          'canvas.get_enrollments',
                          traceback.format_exc())
        finally:
            log_resp_time(logger,
                          'canvas.get_enrollments',
                          timer)
        return []
