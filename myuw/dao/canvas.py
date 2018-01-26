import logging
from uw_canvas.enrollments import Enrollments
from uw_canvas.sections import Sections
from uw_canvas.courses import Courses
from uw_canvas.models import CanvasCourse, CanvasSection
from restclients_core.exceptions import DataFailureException
from myuw.dao.pws import get_regid_of_current_user

logger = logging.getLogger(__name__)


def get_canvas_active_enrollments(request):
    if not hasattr(request, "canvas_act_enrollments"):
        request.canvas_act_enrollments = _enrollments_dict_by_sws_label(
            _get_canvas_active_enrollments_for_regid(
                get_regid_of_current_user(request)))
    return request.canvas_act_enrollments


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
        (sws_label, inst_regid) = sws_section_label(enrollment.sis_section_id)
        if sws_label is not None:
            enrollments_dict[sws_label] = enrollment

    return enrollments_dict


def canvas_prefetch():
    def _method(request):
        return get_canvas_active_enrollments(request)
    return [_method]


def get_canvas_course_from_section(sws_section):
    try:
        return Courses().get_course_by_sis_id(
            sws_section.canvas_course_sis_id())
    except DataFailureException as err:
        if err.status == 404:
            return None

        raise


def get_canvas_course_url(sws_section, person):
    if sws_section.is_independent_study:
        sws_section.independent_study_instructor_regid = person.uwregid

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


def sws_section_label(sis_id):
    canvas_section = CanvasSection(sis_section_id=sis_id)
    sws_label = canvas_section.sws_section_id()
    if sws_label is None:
        canvas_course = CanvasCourse(sis_course_id=sis_id)
        sws_label = canvas_course.sws_course_id()
        return (sws_label, canvas_course.sws_instructor_regid())
    else:
        return (sws_label, canvas_section.sws_instructor_regid())


def get_viewable_course_sections(canvas_course_id, canvas_user_id):
    """
    Returns a list of academic sections in the course identified by
    canvas_course_id, for which the user identified by canvas_user_id can
    view enrollments.
    """
    limit_privileges_to_course_section = False
    limit_sections = {}

    enrollments = Enrollments().get_enrollments_for_course(
        canvas_course_id, params={'user_id': canvas_user_id})

    for enrollment in enrollments:
        if enrollment.limit_privileges_to_course_section:
            limit_privileges_to_course_section = True
            limit_sections[enrollment.section_id] = True

    viewable_sections = []
    for section in Sections().get_sections_in_course(canvas_course_id):
        if not section.is_academic_sis_id():
            continue

        if (limit_privileges_to_course_section and
                section.section_id not in limit_sections):
            continue

        viewable_sections.append(section)

    return viewable_sections
