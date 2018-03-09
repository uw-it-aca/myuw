"""
This module accesses the DB table object UserCourseDisplay
"""
import logging
from myuw.models import UserCourseDisplay
from myuw.dao import get_user_model
from myuw.dao.instructor_schedule import check_section_instructor,\
    get_section_by_label
from myuw.dao.pws import get_person_of_current_user

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
            del existing_color_dict[section_label]
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

    _clean_up_dropped_sections(user, existing_color_dict)


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
    Assign a new color to the section
    """
    UserCourseDisplay.objects.create(user=user,
                                     year=section.term.year,
                                     quarter=section.term.quarter,
                                     section_label=section.section_label(),
                                     color_id=color_id)


def _set_section_colorid(section, color_id):
    if section.is_primary_section:
        section.color_id = color_id
    else:
        section.color_id = "%sa" % color_id


def _clean_up_dropped_sections(user, existing_color_dict):
    """
    The remaining objects in existing_color_dict are no longer needed
    """
    if existing_color_dict:
        for section_label in existing_color_dict.keys():
            obj = UserCourseDisplay.objects.get(user=user,
                                                section_label=section_label)
            obj.delete()


def set_pin_on_teaching_page(request,
                             section_label,
                             pin=True):
    """
    if pin=True, pin the section on teaching page
    if pin=False, unpin the section from teaching page
    @except InvalidSectionID
    @except NotSectionInstructorException
    """
    section = get_section_by_label(section_label)
    check_section_instructor(section, get_person_of_current_user(request))

    # not to pin a primary section
    if section.is_primary_section:
        return False

    obj = UserCourseDisplay.objects.get(user=get_user_model(request),
                                        section_label=section_label)
    if obj:
        if obj.pin_on_teaching_page != pin:
            obj.pin_on_teaching_page = pin
            obj.save()
        return True
    return False
