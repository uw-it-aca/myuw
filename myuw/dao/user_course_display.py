"""
This module accesses the DB table object UserCourseDisplay
"""
import logging
import traceback
from django.db import IntegrityError
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
            existing_color_id = existing_color_dict[section_label]
            color_id = _validated_color(user, primary_color_dict,
                                        section, existing_color_id)

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
                color_id, colors_taken = _get_next_color(colors_taken)
                _record_primary_colors(primary_color_dict, section, color_id)
            _save_section_color(user, section, color_id)

        section.color_id = _make_colorid(section, color_id)


def _get_next_color(colors_taken):
    """
    Return the next available color in the eight color list
    """
    times = int(len(colors_taken) / TOTAL_COURSE_COLORS)
    if len(colors_taken) >= TOTAL_COURSE_COLORS:
        colors_taken = colors_taken[TOTAL_COURSE_COLORS * times:]

    for new_color in range(1, TOTAL_COURSE_COLORS + 1, 1):
        if new_color not in colors_taken:
            colors_taken.append(new_color)
            return new_color, colors_taken


def _make_colorid(section, color_id):
    if section.is_primary_section:
        return color_id
    return "{}a".format(color_id)


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
    if not UserCourseDisplay.exists_section_display(user, section_label):
        try:
            UserCourseDisplay.objects.create(user=user,
                                             year=section.term.year,
                                             quarter=section.term.quarter,
                                             section_label=section_label,
                                             color_id=color_id)
        except Exception as ex:
            logger.warning({'user': user.uwnetid,
                            'at': "create ({} color_id: {}) in DB".format(
                                section_label, color_id),
                            'err': ex})
            if '1062, "Duplicate entry ' not in err:
                raise


def _update_color(user, section_label, color_id):
    UserCourseDisplay.set_color(user, section_label, color_id)


def _validated_color(user, primary_color_dict,
                     sec_section, existing_color_id):
    primary_section_label = sec_section.primary_section_label()
    primary_color_id = primary_color_dict.get(primary_section_label, None)
    if primary_color_id and primary_color_id != existing_color_id:
        _update_color(user, sec_section.section_label(), primary_color_id)
        return primary_color_id
    return existing_color_id
