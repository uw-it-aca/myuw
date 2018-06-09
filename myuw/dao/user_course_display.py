"""
This module accesses the DB table object UserCourseDisplay
"""
import logging
from myuw.models import UserCourseDisplay
from myuw.dao.user import get_user_model

TOTAL_COURSE_COLORS = 8
logger = logging.getLogger(__name__)


def set_course_display_pref(request, schedule):
    """
    Add display elements on the sections in the given schedule
    """
    user = get_user_model(request)
    existing_color_dict, colors_taken, pin_on_teaching_2nds =\
        UserCourseDisplay.get_course_display(user,
                                             schedule.term.year,
                                             schedule.term.quarter)

    primary_color_dict = {}
    # record primary colors used {section_labels: color_id}

    for section in schedule.sections:
        section_label = section.section_label()

        if section_label in pin_on_teaching_2nds:
            section.pin_on_teaching = True
        else:
            section.pin_on_teaching = False

        if section_label in existing_color_dict:
            # exists in DB table
            color_id = existing_color_dict[section_label]
            _record_primary_colors(primary_color_dict, section, color_id)

        else:
            # a section with no color yet
            if not section.is_primary_section:
                primary_label = section.primary_section_label()
            else:
                primary_label = section_label

            if primary_label in primary_color_dict:
                color_id = primary_color_dict[primary_label]
            else:
                color_id = _get_next_color(colors_taken)
                _record_primary_colors(primary_color_dict, section, color_id)

            _save_section_color(user, section, color_id)

        _set_section_colorid(section, color_id)


def _get_next_color(colors_taken):
    """
    Return the next available color in the eight color list
    """
    if len(colors_taken) == TOTAL_COURSE_COLORS:
        colors_taken = []
    for new_color in range(1, TOTAL_COURSE_COLORS + 1, 1):
        if new_color not in colors_taken:
            colors_taken.append(new_color)
            return new_color


def _record_primary_colors(primary_color_dict, section, color_id):
    """
    Remember the primary colors we have used for the term to be
    referenced by the the follow up secondary sections
    """
    if not section.is_primary_section:
        label = section.primary_section_label()
    else:
        label = section.section_label()
    if label not in primary_color_dict:
        primary_color_dict[label] = color_id


def _save_section_color(user, section, color_id):
    """
    Store the color of the section in DB
    """
    section_label = section.section_label()
    if UserCourseDisplay.exists_section_display(user, section_label):
        UserCourseDisplay.set_color(user, section_label, color_id)
        return
    UserCourseDisplay.objects.create(user=user,
                                     year=section.term.year,
                                     quarter=section.term.quarter,
                                     section_label=section_label,
                                     color_id=color_id)


def _set_section_colorid(section, color_id):
    if section.is_primary_section:
        section.color_id = color_id
    else:
        section.color_id = "%sa" % color_id
