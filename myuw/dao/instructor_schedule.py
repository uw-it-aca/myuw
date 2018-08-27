"""
This module provides access to instructed class schedule and sections
"""

import logging
from restclients_core.exceptions import DataFailureException
from uw_sws.models import ClassSchedule
from uw_sws.section import get_sections_by_instructor_and_term,\
    get_section_by_url, get_section_by_label
from uw_sws.section_status import get_section_status_by_label
from myuw.util.thread import ThreadWithResponse
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.registration import get_active_registrations_for_section
from myuw.dao.term import get_current_quarter, get_comparison_datetime
from myuw.dao.user_course_display import set_course_display_pref


logger = logging.getLogger(__name__)


def get_instructor_schedule_by_term(request, term):
    id = "instchedule%d%s" % (term.year, term.quarter)
    if not hasattr(request, id):
        inst_schedule = __get_instructor_schedule_by_term(request, term)
        set_course_display_pref(request, inst_schedule)
        request.id = inst_schedule
    return request.id


def __get_instructor_schedule_by_term(request, term):
    """
    Return the sections (ordered by course abbr, number, section id)
    the current user is instructing in the given term/quarter
    """
    person = get_person_of_current_user(request)
    if person is None or term is None:
        return None

    schedule = ClassSchedule()
    schedule.person = person
    schedule.term = term
    # turn on the checking for future quarters
    term.check_time_schedule_published = term.is_future(
        get_comparison_datetime(request))
    section_references = get_sections_by_instructor_and_term(
        person,
        term,
        future_terms=0,
        include_secondaries=True,
        transcriptable_course='all',
        delete_flag=['active', 'suspended'])

    schedule.sections = _get_sections_by_section_reference(section_references,
                                                           term)
    return schedule


def _get_sections_by_section_reference(section_references, term):
    """
    Return sections in the same order as the section_references
    """
    sections = []
    section_threads = []

    for section_ref in section_references:
        try:
            t = ThreadWithResponse(target=_set_section_from_url,
                                   args=(section_ref.url, term))
            section_threads.append(t)
            t.start()
        except KeyError:
            pass

    for t in section_threads:
        t.join()
        section = t.response
        if section:
            sections.append(section)
    return sections


def _set_section_from_url(section_url, term):
    section = get_section_by_url(section_url)
    if not term.check_time_schedule_published:
        # no need to check
        return section
    else:
        course_campus = section.course_campus.lower()
        # check if the campus specific time schedule is published
        if course_campus not in term.time_schedule_published or\
           term.time_schedule_published[course_campus] is True:
            return section
    return None


def get_instructor_section(request,
                           section_id,
                           include_registrations=False,
                           include_linked_sections=False):
    """
    Return the section that the instructor is teaching
    """
    schedule = ClassSchedule()
    person = get_person_of_current_user(request)
    if person is None:
        return None

    instructor_regid = person.uwregid
    schedule.person = person
    schedule.sections = []

    section = get_section_by_label(section_id)
    schedule.term = section.term

    if include_registrations:
        section.registrations = get_active_registrations_for_section(
            section, instructor_regid)

    schedule.sections.append(section)

    if include_linked_sections:
        threads = []
        for url in section.linked_section_urls:
            t = ThreadWithResponse(target=get_linked_section,
                                   args=(url, instructor_regid))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
            linked = thread.response
            if linked:
                schedule.sections.append(linked)
    set_course_display_pref(request, schedule)
    return schedule


def get_linked_section(url, instructor_regid):
    try:
        linked = get_section_by_url(url)

        try:
            linked.registrations = get_active_registrations_for_section(
                linked, instructor_regid)
        except DataFailureException as ex:
            logger.error("get_linked_section(%s)==>%s", url, ex)
            linked.registrations = []

        return linked
    except Exception:
        return


def check_section_instructor(section, person):
    if not section.is_instructor(person):
        if section.is_primary_section:
            raise NotSectionInstructorException(
                "%s Not Instructor for %s" % (person.uwnetid,
                                              section.section_label()))
        primary_section = get_section_by_label(section.primary_section_label())
        if not primary_section.is_instructor(person):
            raise NotSectionInstructorException(
                "%s Not Instructor for %s" % (
                    person.uwnetid, primary_section.section_label()))


def get_primary_section(secondary_section):
    return get_section_by_label(secondary_section.primary_section_label())
