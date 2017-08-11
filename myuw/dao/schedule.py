"""
This module provides access to registered class schedule and sections
"""

import logging
from uw_sws.models import ClassSchedule
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.term import get_current_quarter, get_next_quarter,\
    get_next_autumn_quarter, get_current_summer_term,\
    is_a_term, is_b_term
from myuw.dao.term import get_comparison_date


logger = logging.getLogger(__name__)


def get_current_quarter_schedule(request):
    """
    Return the actively enrolled sections in the current quarter
    """
    if hasattr(request, "myuw_current_quarter_schedule"):
        return request.myuw_current_quarter_schedule

    schedule = get_schedule_by_term(get_current_quarter(request))
    request.myuw_current_quarter_schedule = schedule

    return schedule


def get_next_quarter_schedule(request):
    """
    Return the actively enrolled sections in the next quarter
    """
    # MUWM-1981
    if get_next_quarter(request) == get_current_quarter(request):
        return None
    return get_schedule_by_term(get_next_quarter(request))


def get_next_autumn_quarter_schedule(request):
    """
    Return the actively enrolled sections in the next autumn quarter
    """
    # MUWM-1981
    if get_next_autumn_quarter(request) == get_current_quarter(request):
        return None
    return get_schedule_by_term(get_next_autumn_quarter(request))


def filter_schedule_sections_by_summer_term(schedule, summer_term):
    """
    Filter the schedule sections by the give summer_term.
    """
    if has_summer_quarter_section(schedule) and\
            is_half_summer_term(summer_term):
        filtered_sections = []
        for section in schedule.sections:
            if section.is_full_summer_term() or\
                    section.is_same_summer_term(summer_term):
                filtered_sections.append(section)
        schedule.sections = filtered_sections


def has_summer_quarter_section(schedule):
    """
    Return True if the given schedule has non-empty summer quarter sections
    """
    return (schedule is not None and
            len(schedule.sections) > 0 and
            schedule.term.is_summer_quarter()
            )


def is_half_summer_term(str):
    """
    return True if the given str is A-term or B-term
    @return True if the given str is A-term or B-term
    """
    return is_a_term(str) or is_b_term(str)
