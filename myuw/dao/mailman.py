"""
This class encapsulates the interactions with
the uwnetid subscription resource.
"""

import logging
import re
from restclients.mailman.list_checker import (get_course_list_name,
                                              exists_course_list)
from myuw.util.thread import Thread
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term


logger = logging.getLogger(__name__)
MAILMAN_ADMIN_URL = "https://mailman.u.washington.edu/mailman/admin/%s"
section_id_ext_pattern = r'.*/course/\d{4},[^/]+/([A-Z][A-Z0-9]?).json$'


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


def get_section_id(url):
    return re.sub(section_id_ext_pattern, r'\1',
                  url, flags=re.IGNORECASE)


def get_all_secondary_section_lists(primary_section):
    secondaries = []
    if primary_section.linked_section_urls:

        if len(primary_section.linked_section_urls) > 1:
            return get_threaded_secondary_section_lists(primary_section)

        if len(primary_section.linked_section_urls) == 1:
            url = primary_section.linked_section_urls[0]
            secondaries.append(
                get_single_email_list(primary_section.curriculum_abbr,
                                      primary_section.course_number,
                                      get_section_id(url),
                                      primary_section.term.quarter,
                                      primary_section.term.year))
    return secondaries


def get_threaded_secondary_section_lists(primary_section):
    secondaries = []
    secondaries_section_ids = []
    list_threads = {}
    for url in primary_section.linked_section_urls:
        section_id = get_section_id(url)
        secondaries_section_ids.append(section_id)
        thread = SingleListThread(primary_section.curriculum_abbr,
                                  primary_section.course_number,
                                  section_id,
                                  primary_section.term.quarter,
                                  primary_section.term.year)
        thread.start()
        list_threads[section_id] = thread

    for section_id in secondaries_section_ids:
        thread = list_threads[section_id]
        thread.join()
        if thread.exception is None:
            secondaries.append(thread.response)
        else:
            logger.error("get_single_email_list(%s,%s,%s,%s,%s)==>%s " %
                         (primary_section.curriculum_abbr,
                          primary_section.course_number,
                          section_id,
                          primary_section.term.quarter,
                          primary_section.term.year,
                          thread.exception))
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
    if len(schedule.sections) == 1:
        json_data["email_lists"].append(
            get_section_email_lists(schedule.sections[0]))

    if len(schedule.sections) > 1:
        section_list = []
        list_threads = {}
        for section in schedule.sections:
            section_label = section.section_label()
            section_list.append(section_label)
            thread = CourseListsThread(section)
            thread.start()
            list_threads[section_label] = thread

        for section_label in section_list:
            thread = list_threads[section_label]
            thread.join()
            if thread.exception is None:
                json_data["email_lists"].append(thread.response)
            else:
                logger.error("get_section_email_lists(%s)==>%s " %
                             (section_label, thread.exception))

    return json_data


class SingleListThread(Thread):

    def __init__(self,
                 curriculum_abbr, course_number, section_id, quarter, year):
        Thread.__init__(self)
        self.curriculum_abbr = curriculum_abbr
        self.course_number = course_number
        self.section_id = section_id
        self.quarter = quarter
        self.year = year
        self.response = None
        self.exception = None

    def run(self):
        try:
            self.response = get_single_email_list(self.curriculum_abbr,
                                                  self.course_number,
                                                  self.section_id,
                                                  self.quarter,
                                                  self.year)
        except Exception as ex:
            self.exception = ex


class CourseListsThread(Thread):

    def __init__(self, section):
        Thread.__init__(self)
        self.section = section
        self.response = None
        self.exception = None

    def run(self):
        try:
            self.response = get_section_email_lists(self.section)
        except Exception as ex:
            self.exception = ex
