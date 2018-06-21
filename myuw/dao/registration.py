"""
This module provides access to uw_sws registration module
"""

import logging
from restclients_core.thread import generic_prefetch
from uw_libraries.subject_guides import get_subject_guide_for_section_params
from uw_sws.registration import get_active_registrations_by_section,\
    get_schedule_by_regid_and_term
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.user_course_display import set_course_display_pref
from myuw.dao.term import get_comparison_datetime

logger = logging.getLogger(__name__)


def get_schedule_by_term(request, term):
    """
    @return a uw_sws.models.ClassSchedule object
    Return the actively enrolled sections for the user
    in the given term/quarter
    """
    regid = get_regid_of_current_user(request)
    id = "myuwschedule%d%s" % (term.year, term.quarter)
    if not hasattr(request, id):
        if term.is_current(get_comparison_datetime(request)):
            non_tsp = True  # include_instructor_not_on_time_schedule

        else:
            non_tsp = False

        student_schedule = get_schedule_by_regid_and_term(
            regid,
            term,
            non_time_schedule_instructors=non_tsp,
            per_section_prefetch_callback=myuw_section_prefetch,
            transcriptable_course="all")
        set_course_display_pref(request, student_schedule)
        request.id = student_schedule
    return request.id


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


def get_active_registrations_for_section(section, instructor_regid):
    if section.is_independent_study:
        section.independent_study_instructor_regid = instructor_regid
    return get_active_registrations_by_section(section,
                                               transcriptable_course="all")
