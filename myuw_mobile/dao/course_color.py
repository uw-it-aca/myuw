"""
This module encapsulates the access of the registration
and section modules in restclients
"""

import logging
import traceback
from myuw_mobile.models import CourseColor
from myuw_mobile.dao.pws import get_regid_of_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception

logger = logging.getLogger(__name__)
TOTAL_COURSE_COLORS = 8


def get_colors_by_schedule(schedule):
    return get_colors_by_regid_and_schedule(
        get_regid_of_current_user(), schedule)


def get_colors_by_regid_and_schedule(regid, schedule):
    if schedule is None or len(schedule.sections) == 0:
        return None
    timer = Timer()
    try:
        return _indexed_colors_by_section_label(
            CourseColor.objects.filter(
                regid=regid,
                year=schedule.term.year,
                quarter=schedule.term.quarter),
            regid,
            schedule)
    except Exception as ex:
        log_exception(logger,
                      'query CourseColor',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      'query CourseColor',
                      timer)
    return None


def _indexed_colors_by_section_label(query, regid, schedule):
    colors = {}
    existing_sections = []
    color_lookup = {}
    active_colors = {}
    colors_to_deactivate = {}
    for color in query:
        existing_sections.append(color)
        if color.is_active:
            color_lookup[color.section_label()] = color
            active_colors[color.color_id] = True
            colors_to_deactivate[color.section_label()] = color

    primary_sections = []
    secondary_sections = []
    for section in schedule.sections:
        if section.is_primary_section:
            primary_sections.append(section)
        else:
            secondary_sections.append(section)

    for section in primary_sections:
        label = section.section_label()
        if section.section_label() not in color_lookup:
            color = _get_section_color(existing_sections,
                                       active_colors,
                                       schedule,
                                       section,
                                       regid)
            existing_sections.append(color)
            color_lookup[color.section_label()] = color
            active_colors[color.color_id] = True

        if section.section_label() in colors_to_deactivate:
            del colors_to_deactivate[section.section_label()]

        colors[label] = color_lookup[section.section_label()].color_id

    for section in secondary_sections:
        label = section.section_label()
        primary_label = section.primary_section_label()

        if colors[primary_label] is None:
            # ... uh oh
            pass

        colors[label] = "%sa" % colors[primary_label]

    for color_key in colors_to_deactivate:
        color = colors_to_deactivate[color_key]
        color.is_active = False
        color.save()

    return colors


def _get_section_color(existing_sections, active,
                       schedule, section, regid):
    color = CourseColor()
    color.regid = regid
    color.year = schedule.term.year
    color.quarter = schedule.term.quarter
    color.curriculum_abbr = section.curriculum_abbr
    color.course_number = section.course_number
    color.section_id = section.section_id
    color.is_active = True
    next_color = len(existing_sections) + 1

    if next_color > TOTAL_COURSE_COLORS:
        for add in range(TOTAL_COURSE_COLORS):
            total = next_color + add
            test_color = (total % TOTAL_COURSE_COLORS) + 1

            if test_color not in active:
                next_color = test_color
                break

    if next_color > TOTAL_COURSE_COLORS:
        next_color = ((next_color - 1) % TOTAL_COURSE_COLORS) + 1

    color.color_id = next_color
    color.save()

    return color
