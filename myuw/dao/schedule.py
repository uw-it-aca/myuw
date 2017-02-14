"""
This module provides access to registered class schedule and sections
"""

import logging
from restclients.models.sws import ClassSchedule
from restclients.sws.registration import get_schedule_by_regid_and_term
from restclients.thread import generic_prefetch
from restclients.library.currics import get_subject_guide_for_section_params
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_current_quarter, get_next_quarter,\
    get_next_autumn_quarter, get_current_summer_term,\
    is_a_term, is_b_term
from myuw.dao.term import get_comparison_date
from restclients.exceptions import DataFailureException


logger = logging.getLogger(__name__)
EARLY_FALL_START = "EARLY FALL START"


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
        courses = get_schedule_by_regid_and_term(regid, term, False,
                                                 myuw_section_prefetch)
        # retrieve non-transcriptable courses
        try:
            nts_courses = get_schedule_by_regid_and_term(regid, term, False,
                                                         myuw_section_prefetch,
                                                         "no")
            # combine non-transcriptable courses and transcriptable courses
            for section in nts_courses.sections:
                courses.sections.append(section)

        except DataFailureException as ex:
            # This will be thrown when mock data does not exist
            pass

        return courses

    finally:
        log_resp_time(logger,
                      logid,
                      timer)


def myuw_section_prefetch(data):
    primary = data["PrimarySection"]
    params = [primary["Year"],
              primary["Quarter"],
              primary["CurriculumAbbreviation"],
              primary["CourseNumber"],
              data["SectionID"]
              ]

    key = "library-%s-%s-%s-%s-%s" % (tuple(params))
    method = generic_prefetch(get_subject_guide_for_section_params,
                              params)

    return [[key, method]]


def get_schedule_by_term(request, term):
    """
    Return the actively enrolled sections for the current user
    in the given term/quarter
    """
    # 2016 approach for MUWM-3390/3391
    # If we're in the EFS period, include the sections.  Otherwise,
    # exclude them.
    schedule = _get_schedule(get_regid_of_current_user(), term)
    comparison_date = get_comparison_date(request)

    included_sections = []
    for section in schedule.sections:
        if EARLY_FALL_START != section.institute_name:
            included_sections.append(section)
        else:
            end_date = section.end_date
            if end_date >= comparison_date:
                included_sections.append(section)

    schedule.sections = included_sections

    return schedule


def get_current_quarter_schedule(request):
    """
    Return the actively enrolled sections in the current quarter
    """
    if hasattr(request, "myuw_current_quarter_schedule"):
        return request.myuw_current_quarter_schedule

    schedule = get_schedule_by_term(request, get_current_quarter(request))
    request.myuw_current_quarter_schedule = schedule

    return schedule


def get_next_quarter_schedule(request):
    """
    Return the actively enrolled sections in the next quarter
    """
    # MUWM-1981
    if get_next_quarter(request) == get_current_quarter(request):
        return None
    return get_schedule_by_term(request, get_next_quarter(request))


def get_next_autumn_quarter_schedule(request):
    """
    Return the actively enrolled sections in the next autumn quarter
    """
    # MUWM-1981
    if get_next_autumn_quarter(request) == get_current_quarter(request):
        return None
    return get_schedule_by_term(request, get_next_autumn_quarter(request))


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
