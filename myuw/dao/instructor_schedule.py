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
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.instructor import is_seen_instructor, add_seen_instructor
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.registration import get_active_registrations_for_section
from myuw.dao.term import get_current_quarter


logger = logging.getLogger(__name__)


def get_instructor_schedule_by_term(request, term):
    """
    Return the sections the current user is instructing
    in the given term/quarter
    """
    person = get_person_of_current_user(request)
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


def get_instructor_section(request, section_id,
                           include_registrations=False,
                           include_linked_sections=False):
    """
    Return requested section instructor is teaching
    """
    schedule = ClassSchedule()
    person = get_person_of_current_user(request)
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


def get_limit_estimate_enrollment_for_section(section):
    section_status = get_section_status_by_label(section.section_label())
    return section_status.limit_estimated_enrollment


def is_instructor(request):
    """
    Determines if user is an instructor of the request's term
    """
    if hasattr(request, "myuw_is_instructor"):
        return request.myuw_is_instructor

    try:
        person = get_person_of_current_user(request)
        user_netid = person.uwnetid
        if is_seen_instructor(user_netid):
            request.myuw_is_instructor = True
            return True

        term = get_current_quarter(request)
        sections = _get_instructor_sections(person,
                                            term,
                                            future_terms=2,
                                            include_secondaries=False)
        if len(sections) > 0:
            add_seen_instructor(user_netid, term)
            request.myuw_is_instructor = True
            return True
        request.myuw_is_instructor = False
        return False
    except DataFailureException as err:
        if err.status == 404:
            request.myuw_is_instructor = False
            return False
        raise


def is_instructor_prefetch():
    def _method(request):
        is_instructor(request)
    return [_method]


def check_section_instructor(section, person):
    if not section.is_instructor(person):
        if section.is_primary_section:
            raise NotSectionInstructorException()
        primary_section = get_section_by_label(section.primary_section_label())
        if not primary_section.is_instructor(person):
            raise NotSectionInstructorException()


def get_primary_section(secondary_section):
    return get_section_by_label(secondary_section.primary_section_label())
