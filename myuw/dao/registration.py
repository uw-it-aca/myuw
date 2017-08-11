"""
This module provides access to uw_sws registration module
"""

import logging
from restclients_core.thread import generic_prefetch
from uw_libraries.subject_guides import get_subject_guide_for_section_params
from uw_sws.registration import get_active_registrations_by_section,\
    get_schedule_by_regid_and_term
from myuw.dao.pws import get_regid_of_current_user


logger = logging.getLogger(__name__)


def get_schedule_by_term(term):
    """
    Return the actively enrolled sections for the current user
    in the given term/quarter
    """
    return _get_schedule(get_regid_of_current_user(), term)


def _get_schedule(regid, term):
    """
    @return a uw_sws.models.ClassSchedule object
    Return the actively enrolled sections for the current user
    in the given term/quarter
    """
    if regid is None or term is None:
        return None
    logid = ('get_schedule_by_regid_and_term ' +
             str(regid) + ',' + str(term.year) + ',' + term.quarter)
    return get_schedule_by_regid_and_term(
        regid,
        term,
        non_time_schedule_instructors=False,
        per_section_prefetch_callback=myuw_section_prefetch,
        transcriptable_course="all")


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
