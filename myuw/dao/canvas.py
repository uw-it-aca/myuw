# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import re
import traceback
from restclients_core.exceptions import DataFailureException
from uw_canvas.enrollments import Enrollments
from uw_canvas.sections import Sections
from uw_canvas.courses import Courses
from uw_canvas.models import CanvasCourse, CanvasSection
from uw_sws.exceptions import (
    InvalidCanvasIndependentStudyCourse, InvalidCanvasSection)
from myuw.dao import log_err
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_comparison_datetime

logger = logging.getLogger(__name__)
canvas_enrollments = Enrollments()


def canvas_prefetch():
    def _method(request):
        return get_canvas_active_enrollments(request)
    return [_method]


def get_canvas_active_enrollments(request):
    if not hasattr(request, "canvas_act_enrollments"):
        request.canvas_act_enrollments = (
            canvas_enrollments.get_enrollments_for_regid(
                get_regid_of_current_user(request),
                {'type': ['StudentEnrollment'], 'state': ['active']}))
        logger.info({'canvas_act_enrollments':
                     request.canvas_act_enrollments[0].json_data()})
    return request.canvas_act_enrollments


def set_section_canvas_course_urls(canvas_active_enrollments, schedule,
                                   request):
    """
    Set canvas_course_url in schedule.sections
    """
    canvas_sis_ids = {}
    # MUWM-5362 {canvas_section_sis_id: primary_section_label}
    for section in schedule.sections:
        section_label = section.section_label()

        try:
            cid = section.canvas_course_sis_id()
            if cid not in canvas_sis_ids:
                canvas_sis_ids[cid] = section.primary_section_label()
        except InvalidCanvasIndependentStudyCourse as ex:
            # REQ3132940 known SWS issue:
            # prior quarter's registration data has
            # no independent study instructor.
            # If independent_study_instructor being None occurs
            # in current or future quarter, likely is a data error.
            log_err(
                logger, f"canvas_course_sis_id of {section_label} {ex}",
                traceback, request)
            continue
        try:
            cid = section.canvas_section_sis_id()
            canvas_sis_ids[cid] = section.primary_section_label()
        except Exception as ex:
            log_err(
                logger, f"canvas_section_sis_id of {section_label} {ex}",
                traceback, request)

    logger.info({'canvas_sis_ids': canvas_sis_ids})

    canvas_links = {}  # primary_section_label: canvas course_url
    for enrollment in canvas_active_enrollments:
        psection_label = None
        # MUWM-5362 check both course and section
        if enrollment.sis_section_id in canvas_sis_ids:
            psection_label = canvas_sis_ids[enrollment.sis_section_id]
        else:
            if enrollment.sis_course_id in canvas_sis_ids:
                psection_label = canvas_sis_ids[enrollment.sis_course_id]
        if psection_label and psection_label not in canvas_links:
            canvas_links[psection_label] = enrollment.course_url
    logger.info({'canvas_links': canvas_links})
    for section in schedule.sections:
        section.canvas_course_url = canvas_links.get(
            section.primary_section_label())


def get_canvas_course_from_section(sws_section):
    try:
        return Courses().get_course_by_sis_id(
            sws_section.canvas_course_sis_id())
    except DataFailureException as err:
        if err.status == 404:
            return None
        raise ValueError


def get_canvas_course_url(sws_section, person):
    if sws_section.is_independent_study:
        sws_section.independent_study_instructor_regid = person.uwregid
    try:
        canvas_course = get_canvas_course_from_section(sws_section)
    except ValueError:
        return "error"
    if canvas_course:
        return canvas_course.course_url


def sws_section_label(sis_id):
    canvas_section = CanvasSection(sis_section_id=sis_id)
    sws_label = canvas_section.sws_section_id()
    if sws_label is not None:
        return (sws_label, canvas_section.sws_instructor_regid())
    canvas_course = CanvasCourse(sis_course_id=sis_id)
    sws_label = canvas_course.sws_course_id()
    return (sws_label, canvas_course.sws_instructor_regid())


def get_viewable_course_sections(canvas_course_id, canvas_user_id):
    """
    Returns a list of academic sections in the course identified by
    canvas_course_id, for which the user identified by canvas_user_id can
    view enrollments.
    """
    limit_privileges_to_course_section = False
    limit_sections = {}

    enrollments = canvas_enrollments.get_enrollments_for_course(
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
