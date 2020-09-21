"""
This module provides access to uw_sws registration module
"""

from copy import deepcopy
import logging
from restclients_core.thread import generic_prefetch
from uw_libraries.subject_guides import get_subject_guide_for_section_params
from uw_sws.registration import get_schedule_by_regid_and_term
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import get_comparison_datetime, get_current_quarter
from myuw.dao.user_course_display import set_course_display_pref

logger = logging.getLogger(__name__)


def get_schedule_by_term(request, term=None, summer_term=None, tsprint=True):
    """
    :return: the student's class schedule (uw_sws.models.ClassSchedule) of
    the actively enrolled sections for the user in the given quarter
    and corresponding summer term.
    :param Term term: None uses current term related to the given request
    :param str summer_term: 'full-term': includes all sections;
    'a-term', 'b-term': expects a term-specific schedule;
    None: expects a term-specific schedule if currently in the summer term.
    """
    student_schedule = get_schedule_by_regid_and_term(
        get_regid_of_current_user(request),
        term if term is not None else get_current_quarter(request),
        per_section_prefetch_callback=myuw_section_prefetch,
        transcriptable_course="all")

    if (len(student_schedule.sections) and
            student_schedule.term.is_summer_quarter()):
        filter_sections_by_summer_term(request, student_schedule, summer_term)

    if len(student_schedule.sections):
        set_course_display_pref(request, student_schedule)
        if tsprint:
            _exclude_not_tsprint_instructors(student_schedule)

    return student_schedule


def myuw_section_prefetch(data):
    primary = data["PrimarySection"]
    params = [primary["Year"],
              primary["Quarter"],
              primary["CurriculumAbbreviation"],
              primary["CourseNumber"],
              data["SectionID"]
              ]

    key = "library-{}-{}-{}-{}-{}".format(tuple(params))
    method = generic_prefetch(get_subject_guide_for_section_params,
                              params)
    return [[key, method]]


def _exclude_not_tsprint_instructors(schedule):
    for section in schedule.sections:
        # filter out TSPrint=False instructors on non-independent study
        if not section.is_independent_study:
            for meeting in section.meetings:
                for instructor in deepcopy(meeting.instructors):
                    if not instructor.TSPrint:
                        meeting.instructors.remove(instructor)


def filter_sections_by_summer_term(request, schedule, summer_term):
    """
    :param str summer_term: if not "full-term", this function will
    exclude the sections belong to the other summer-term.
    """
    summer_term = _get_current_summer_term(request, schedule, summer_term)
    schedule.summer_term = summer_term
    if summer_term != "full-term":
        sections_to_keep = []
        for section in schedule.sections:
            if (section.is_full_summer_term() or
                    section.is_same_summer_term(summer_term)):
                sections_to_keep.append(section)
            else:
                sst = section.summer_term.lower()
                schedule.registered_summer_terms[sst] = False
        schedule.sections = sections_to_keep


def _get_current_summer_term(request, schedule, summer_term):
    if summer_term is not None and len(summer_term):
        return summer_term.lower()

    if _is_split_term(schedule.registered_summer_terms):
        aterm_end = schedule.term.get_eod_summer_aterm()
        if get_comparison_datetime(request) > aterm_end:
            return "b-term"
        else:
            return "a-term"
    return "full-term"


def _is_split_term(registered_summer_terms):
    """
    Return True if the schedule needs to be displayed with
    separate summer terms if the user has:
      only a-term and/or b-term sections or
      a-term and full-term sections or
      b-term and full-term sections
    """
    has_a_term_course = registered_summer_terms.get('a-term') is True
    has_b_term_course = registered_summer_terms.get('b-term') is True
    return has_a_term_course or has_b_term_course
