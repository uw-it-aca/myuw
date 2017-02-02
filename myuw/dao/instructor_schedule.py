"""
This module provides access to instructed class schedule and sections
"""

from django.conf import settings
import logging
from restclients.sws.section import get_sections_by_instructor_and_term,\
    get_section_by_url
from restclients.sws.section_status import get_section_status_by_label
from restclients.sws.section import get_section_by_label
from restclients.models.sws import ClassSchedule
from restclients.exceptions import DataFailureException
from restclients.sws.term import get_specific_term
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.term import get_current_quarter
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.util.thread import Thread


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
    section_references = _get_instructor_sections(person, term)
    if len(section_references) <= getattr(
            settings, "MYUW_MAX_INSTRUCTOR_SECTIONS", 10):
        schedule.sections = _get_sections_by_section_reference(
            section_references)
    else:
        schedule.sections = []
        schedule.section_references = section_references

    return schedule


def _set_section_from_url(sections, section_url):
    sections.append(get_section_by_url(section_url))


def _get_sections_by_section_reference(section_references):
    sections = []
    section_threads = []

    for section_ref in section_references:
        try:
            t = Thread(target=_set_section_from_url,
                       args=(sections, section_ref.url))
            section_threads.append(t)
            t.start()
        except KeyError:
            pass

    for t in section_threads:
        t.join()

    return sections


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


def get_instructor_section(year, quarter, curriculum,
                           course_number, course_section):
    """
    Return requested section instructor is teaching
    """
    schedule = ClassSchedule()
    schedule.person = get_person_of_current_user()
    schedule.term = get_specific_term(year, quarter)
    schedule.sections = []
    section = get_section_by_label("%s,%s,%s,%s/%s" % (
        year, quarter.lower(), curriculum.upper(),
        course_number, course_section))

    if not section.is_instructor(schedule.person):
        raise NotSectionInstructorException()

    schedule.sections.append(section)
    return schedule


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
