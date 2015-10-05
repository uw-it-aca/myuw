"""
This module provides access to registered class schedule and sections
"""

import logging
import traceback
from restclients.models.sws import ClassSchedule
from restclients.sws.registration import get_schedule_by_regid_and_term
from restclients.sws.section import is_half_summer_term,\
    is_full_summer_term, is_same_summer_term
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_current_quarter, get_next_quarter,\
    get_next_autumn_quarter, get_current_summer_term


logger = logging.getLogger(__name__)


def _get_schedule(regid, term):
    """
    @return a restclients.models.sws.ClassSchedule object
    Return the actively enrolled sections for the current user
    in the given term/quarter
    """
    if regid is None or term is None:
        return None
    logid = ('get_schedule_by_regid_and_term ' +
             str(regid) + ',' + str(term.year) + ',' + term.quarter)
    timer = Timer()
    try:
        return get_schedule_by_regid_and_term(regid, term, False)
    except Exception as ex:
        log_exception(logger,
                      logid,
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      logid,
                      timer)
    return None


def get_schedule_by_term(term):
    """
    Return the actively enrolled sections for the current user
    in the given term/quarter
    """
    return _get_schedule(get_regid_of_current_user(), term)


def get_current_quarter_schedule(request):
    """
    Return the actively enrolled sections in the current quarter
    """
    return get_schedule_by_term(get_current_quarter(request))


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
    if (has_summer_quarter_section(schedule) and
            is_half_summer_term(summer_term)):
        filtered_sections = []
        for section in schedule.sections:
            if (is_full_summer_term(section.summer_term) or
                    is_same_summer_term(section.summer_term, summer_term)):
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
