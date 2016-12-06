import logging
from restclients.canvas.courses import Courses
from myuw.dao.pws import get_regid_of_current_user
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time
import re


logger = logging.getLogger(__name__)


def get_canvas_enrolled_courses():
    timer = Timer()
    try:
        return Courses().get_courses_for_regid(
            get_regid_of_current_user(),
            {'enrollment_type': 'student',
             'enrollment_state': 'active',
             'include': ['sections', 'term']},
            verbatim=True)
    finally:
        log_resp_time(logger,
                      'get_canvas_enrolled_courses',
                      timer)


class CanvasCourses(object):
    def __init__(self):
        """
        Returns active course information for the current user.
        Raises: DataFailureException
        """
        self.courses_dict = {}
        self.courses = get_canvas_enrolled_courses()
        for course in self.courses:
            course.sections_dict = {self._sws_id_from_course_code(
                course, s.name): s for s in course.sections}
            self.courses_dict[self._sws_id_from_course_code(
                course, course.code)] = course

    def get_url_for_section(self, sws_section_id):
        course = self._course_from_sws_section_id(sws_section_id)
        return course.course_url if course else None

    def get_name_for_section(self, sws_section_id):
        course = self._course_from_sws_section_id(sws_section_id)
        return course.name if course else ''

    def _course_from_sws_section_id(self, sws_section_id):
        try:
            return self.courses_dict[sws_section_id]
        except KeyError:
            for course_id, course in self.courses_dict.iteritems():
                try:
                    if course.sections_dict[sws_section_id]:
                        return course
                except KeyError:
                    pass

        return None

    def _sws_id_from_course_code(self, course, course_code):
        term = course.term.name.split(' ')
        code = re.match(r'^(.*) ([0-9]+) ([0-9A-Z]+)( \([a-z]+ [0-9]+\))?$',
                        course_code)
        if code:
            return "%s,%s,%s,%s/%s" % (
                term[1], term[0].lower(), code.group(1), code.group(2),
                code.group(3)) if code else ''

        return course.name


def canvas_courses_prefetch():
    return [get_canvas_enrolled_courses]


def _indexed_by_course_id(enrollments):
    """
    return a dictionary of SWS course id to enrollment.
    """
    canvas_data_by_course_id = {}
    if enrollments and len(enrollments) > 1:
        for enrollment in enrollments:
            canvas_data_by_course_id[enrollment.sws_course_id()] = enrollment
    return canvas_data_by_course_id
