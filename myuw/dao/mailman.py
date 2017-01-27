"""
This class encapsulates the interactions with
the uwnetid subscription resource.
"""

import logging
import re
from restclients.models.sws import Section, Term
from myuw.dao.pws import get_person_of_current_user
from restclients.mailman.list_checker import exists_section_list,\
    exists_secondary_section_combined_list, get_section_list_name,\
    exists_instructor_term_combined_list, get_instructor_term_list_name,\
    get_secondary_section_combined_list_name
from myuw.dao.instructor_schedule import _get_instructor_schedule


logger = logging.getLogger(__name__)


def _get_section(term, curriculum_abbr, course_number, section_id):
    return Section(term=term,
                   curriculum_abbr=curriculum_abbr,
                   course_number=course_number,
                   section_id=section_id)


def get_single_email_list_by_section(section):
    """
    @return json of the section specfic email list info
    """
    return {
        "section_id": section.section_id,
        "list_address": get_section_list_name(section),
        "list_exists": exists_section_list(section)
        }


def get_email_list(term, curriculum_abbr, course_number, section_id):
    return get_single_email_list_by_section(
        _get_section(term, curriculum_abbr, course_number, section_id))


def get_email_lists_by_term(term):
    """
    @return json of the corresponding email lists
    associated with the current instructor in the given term
    """
    person = get_person_of_current_user()
    schedule = _get_instructor_schedule(person, term)
    json_data = {
        "year": term.year,
        "quarter": term.quarter,
        }
    json_data["email_lists"] = []
    for section in schedule.sections:
        json_data["email_lists"].append(
            get_section_email_lists(section))
    return json_data


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


section_id_ext_pattern = r'.*/course/\d{4},[^/]+/([A-Z][A-Z0-9]?).json$'


def get_all_secondary_section_lists(primary_section):
    secondaries = []
    if primary_section.linked_section_urls and\
            len(primary_section.linked_section_urls):
        for url in primary_section.linked_section_urls:
            section_id = re.sub(section_id_ext_pattern, r'\1',
                                url, flags=re.IGNORECASE)
            section = _get_section(primary_section.term,
                                   primary_section.curriculum_abbr,
                                   primary_section.course_number,
                                   section_id)
            secondaries.append(get_single_email_list_by_section(section))
    return secondaries


def email_list_prefetch(term):

    def _method(request):
        get_email_lists_by_term(term)

    return [_method]
