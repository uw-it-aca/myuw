"""
This module provides access to instructed class schedule and sections
"""

from django.conf import settings
import logging
from uw_sws.section import get_sections_by_instructor_and_term,\
    get_section_by_url
from uw_sws.registration import get_active_registrations_by_section
from uw_sws.section import get_section_by_label
from uw_sws.term import get_specific_term
from uw_sws.section_status import get_section_status_by_label
from uw_sws.models import ClassSchedule
from restclients_core.exceptions import DataFailureException
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.term import get_current_quarter
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.util.thread import Thread, ThreadWithResponse


logger = logging.getLogger(__name__)


def _get_instructor_sections(person, term):
    """
    @return a uw_sws.models.ClassSchedule object
    Return the actively enrolled sections for the current user
    in the given term/quarter
    """
    if person is None or term is None:
        return None
    return get_sections_by_instructor_and_term(person, term)


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

    if include_registrations:
        section.registrations = get_active_registrations_by_section(section)

    if not section.is_instructor(schedule.person):
        raise NotSectionInstructorException()

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
