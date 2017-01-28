"""
This class encapsulates the interactions with
the uwnetid subscription resource.
"""

import logging
import re
from restclients.mailman.list_checker import (get_course_list_name,
                                              exists_course_list)
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term


logger = logging.getLogger(__name__)
MAILMAN_ADMIN_URL = "https://mailman.u.washington.edu/mailman/admin/%s"


def get_single_email_list(curriculum_abbr, course_number, section_id,
                          quarter, year):
    exists = exists_course_list(curriculum_abbr, course_number,
                                section_id, quarter, year)
    list_name = get_course_list_name(curriculum_abbr, course_number,
                                     section_id, quarter, year)
    list_admin_url = None
    if exists:
        list_admin_url = MAILMAN_ADMIN_URL % list_name

    return {
        "list_exists": exists,
        "list_address": list_name,
        "list_admin_url": list_admin_url
        }


section_id_ext_pattern = r'.*/course/\d{4},[^/]+/([A-Z][A-Z0-9]?).json$'


def get_all_secondary_section_lists(primary_section):
    secondaries = []
    if primary_section.linked_section_urls and\
            len(primary_section.linked_section_urls):
        for url in primary_section.linked_section_urls:
            section_id = re.sub(section_id_ext_pattern, r'\1',
                                url, flags=re.IGNORECASE)
            secondaries.append(
                get_single_email_list(primary_section.curriculum_abbr,
                                      primary_section.course_number,
                                      section_id,
                                      primary_section.term.quarter,
                                      primary_section.term.year))
    return secondaries


def get_single_email_list_by_section(section):
    """
    @return json of the section specfic email list info
    """
    return get_single_email_list(section.curriculum_abbr,
                                 section.course_number,
                                 section.section_id,
                                 section.term.quarter,
                                 section.term.year)


def get_section_email_lists(section):
    """
    @param section: a valid sws.Section object
    """
    is_primary_section = section.is_primary_section
    json_data = {
        "course_abbr": section.curriculum_abbr,
        "course_number": section.course_number,
        "section_id": section.section_id,
        "is_primary": is_primary_section,
        }
    if is_primary_section:
        json_data["primary_list"] = get_single_email_list_by_section(section)

        json_data["secondary_lists"] =\
            get_all_secondary_section_lists(section)

        json_data["has_multi_secondaries"] =\
            (len(json_data["secondary_lists"]) > 1)

    else:
        json_data["section_list"] = get_single_email_list_by_section(section)
    return json_data


def get_email_lists_by_term(term):
    """
    @return json of the corresponding email lists
    associated with the current instructor in the given term
    """
    schedule = get_instructor_schedule_by_term(term)
    json_data = {
        "year": term.year,
        "quarter": term.quarter,
        }
    json_data["email_lists"] = []
    for section in schedule.sections:
        json_data["email_lists"].append(
            get_section_email_lists(section))
    return json_data
