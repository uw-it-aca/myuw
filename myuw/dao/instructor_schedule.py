"""
This module provides access to instructed class schedule and sections
"""

import logging
from restclients.sws.section import get_sections_by_instructor_and_term,\
    get_section_by_url
from restclients.sws.section_status import get_section_status_by_label
from restclients.models.sws import ClassSchedule
from restclients.exceptions import DataFailureException
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.term import get_current_quarter, get_next_quarter,\
    get_next_autumn_quarter

logger = logging.getLogger(__name__)


def _get_instructor_sections(person, term):
    """
    @return a restclients.models.sws.ClassSchedule object
    Return the actively enrolled sections for the current user
    in the given term/quarter
    """
    if person is None or term is None:
        return None
    logid = ('get_instructor_schedule_by_person_and_term ' +
             str(person.uwnetid) + ',' + str(term.year) + ',' + term.quarter)
    timer = Timer()
    try:
        return get_sections_by_instructor_and_term(person, term)
    finally:
        log_resp_time(logger,
                      logid,
                      timer)


def _get_instructor_schedule(person, term):
    schedule = ClassSchedule()
    schedule.person = person
    schedule.term = term
    schedule.sections = []
    for section_ref in _get_instructor_sections(person, term):
        schedule.sections.append(get_section_by_url(section_ref.url))

    return schedule


def get_instructor_schedule_by_term(term):
    """
    Return the sections the current user is instructing
    in the given term/quarter
    """

    person = get_person_of_current_user()
    schedule = _get_instructor_schedule(person, term)
    return schedule


def get_current_quarter_instructor_schedule(request):
    """
    Return sections instructor is teaching in the current quarter
    """
    if hasattr(request, "myuw_current_quarter_instructor_schedule"):
        return request.myuw_current_quarter_instructor_schedule

    schedule = get_instructor_schedule_by_term(get_current_quarter(request))
    request.myuw_current_quarter_instructor_schedule = schedule

    return schedule


def get_next_quarter_instructor_instructor_schedule(request):
    """
    Return sections instructor is teaching in the next quarter
    """
    # MUWM-1981
    if get_next_quarter(request) == get_current_quarter(request):
        return None
    return get_instructor_schedule_by_term(get_next_quarter(request))


def get_next_autumn_quarter_instructor_schedule(request):
    """
    Return sections instructor is teaching in the next autumn quarter
    """
    # MUWM-1981
    if get_next_autumn_quarter(request) == get_current_quarter(request):
        return None
    return get_instructor_schedule_by_term(get_next_autumn_quarter(request))


def get_limit_estimate_enrollment_for_section(section):
    section_status = get_section_status_by_label(section.section_label())
    return section_status.limit_estimated_enrollment


def is_instructor(request):
    """
    Return sections instructor is teaching in the next autumn quarter
    """
    try:
        person = get_person_of_current_user()
        term = get_current_quarter(request)
        sections = _get_instructor_sections(person, term)
        return (len(sections) > 0)
    except DataFailureException as err:
        if err.status == 404:
            return False

        raise
