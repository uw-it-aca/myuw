"""
This module provides access to instructed class schedule and sections
"""

import logging
from restclients_core.exceptions import DataFailureException
from uw_sws.models import ClassSchedule
from uw_sws.section import get_sections_by_instructor_and_term,\
    get_section_by_url, get_section_by_label
from uw_sws.section_status import get_section_status_by_label
from myuw.util.thread import Thread, ThreadWithResponse
from myuw.dao import get_netid_of_current_user
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.instructor import is_seen_instructor, add_seen_instructor
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.registration import get_active_registrations_for_section
from myuw.dao.term import get_current_quarter, get_specific_term


logger = logging.getLogger(__name__)


def get_current_quarter_instructor_schedule(request):
    """
    Return sections instructor is teaching in the current quarter
    """
    if hasattr(request, "myuw_current_quarter_instructor_schedule"):
        return request.myuw_current_quarter_instructor_schedule

    schedule = get_instructor_schedule_by_term(get_current_quarter(request))
    request.myuw_current_quarter_instructor_schedule = schedule

    return schedule


def get_instructor_schedule_by_term(term):
    """
    Return the sections the current user is instructing
    in the given term/quarter
    """
    person = get_person_of_current_user()
    schedule = _get_instructor_schedule(person, term)
    return schedule


def _get_instructor_schedule(person, term):
    schedule = ClassSchedule()
    schedule.person = person
    schedule.term = term

    section_references = _get_instructor_sections(person, term)
    schedule.sections = _get_sections_by_section_reference(section_references)
    return schedule


def _get_instructor_sections(person, term,
                             future_terms=0,
                             include_secondaries=True):
    """
    @return a uw_sws.models.ClassSchedule object
    Return the actively enrolled sections for the current user
    in the given term/quarter
    """
    if person is None or term is None:
        return None
    return get_sections_by_instructor_and_term(
        person,
        term,
        future_terms=future_terms,
        include_secondaries=include_secondaries,
        transcriptable_course='all')


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


def get_instructor_section(year, quarter, curriculum,
                           course_number, course_section,
                           include_registrations=False,
                           include_linked_sections=False):
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

    check_section_instructor(section, schedule.person)

    if include_registrations:
        section.registrations = get_active_registrations_for_section(
            section, schedule.person.uwregid)

    schedule.sections.append(section)
    if include_linked_sections:
        threads = []
        for url in section.linked_section_urls:
            t = ThreadWithResponse(target=get_linked_section, args=(url,))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
            linked = thread.response
            if linked:
                schedule.sections.append(linked)

    return schedule


def get_linked_section(url):
    try:
        linked = get_section_by_url(url)
        registrations = get_active_registrations_by_section(linked)
        linked.registrations = registrations

        return linked
    except:
        return


def get_limit_estimate_enrollment_for_section(section):
    section_status = get_section_status_by_label(section.section_label())
    return section_status.limit_estimated_enrollment


def is_instructor(request):
    """
    Determines if user is an instructor of the request's term
    """
    try:
        term = get_current_quarter(request)
        user_netid = get_netid_of_current_user()
        if is_seen_instructor(user_netid):
            return True

        person = get_person_of_current_user()
        sections = _get_instructor_sections(person,
                                            term,
                                            future_terms=2,
                                            include_secondaries=False)
        if len(sections) > 0:
            add_seen_instructor(user_netid, term)
            return True

        return False
    except DataFailureException as err:
        if err.status == 404:
            return False

        raise


def check_section_instructor(section, person=None):
    if person is None:
        person = get_person_of_current_user()
    if not section.is_instructor(person):
        if section.is_primary_section:
            raise NotSectionInstructorException()
        primary_section = get_section_by_label(section.primary_section_label())
        if not primary_section.is_instructor(person):
            raise NotSectionInstructorException()
