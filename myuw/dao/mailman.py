"""
This class encapsulates the interactions with
the uwnetid subscription resource.
"""

import logging
import re
from django.core.mail import send_mail
from django.conf import settings
from restclients.sws.section import get_section_by_label,\
    is_valid_section_label
from restclients.mailman.basic_list import get_admin_url
from restclients.mailman.course_list import get_course_list_name,\
    exists_course_list, get_section_secondary_combined_list_name,\
    exists_section_secondary_combined_list, get_section_list_name
from restclients.mailman.instructor_term_list import\
    get_instructor_term_list_name, exists_instructor_term_list
from myuw.util.thread import ThreadWithResponse
from myuw.dao.exceptions import CourseRequestEmailRecipientNotFound


logger = logging.getLogger(__name__)
section_id_ext_pattern = r'.*/course/\d{4},[^/]+/([A-Z][A-Z0-9]?).json$'


def get_list_json(exists, list_name):
    return {
        "list_exists": exists,
        "list_address": list_name,
        "list_admin_url": get_admin_url(list_name) if exists else None
        }


def get_instructor_term_list(netid, quarter, year):
    exists = exists_instructor_term_list(netid, year, quarter)
    return get_list_json(
        exists, get_instructor_term_list_name(netid, year, quarter))


def get_section_secondary_combined_list(primary_section):
    exists = exists_section_secondary_combined_list(primary_section)
    return get_list_json(
        exists, get_section_secondary_combined_list_name(primary_section))


def get_section_label(curriculum_abbr, course_number,
                      section_id, quarter, year):
    return "%s,%s,%s,%s/%s" % (
        year, quarter.lower(), curriculum_abbr, course_number, section_id)


def get_single_course_list(curriculum_abbr, course_number, section_id,
                           quarter, year):
    exists = exists_course_list(curriculum_abbr, course_number,
                                section_id, quarter, year)
    data = get_list_json(
        exists, get_course_list_name(curriculum_abbr, course_number,
                                     section_id, quarter, year))
    data["section_id"] = section_id
    data["section_label"] = get_section_label(
        curriculum_abbr, course_number, section_id, quarter, year)
    return data


def get_single_section_list(section):
    """
    @return json of the section specfic email list info
    """
    return get_single_course_list(section.curriculum_abbr,
                                  section.course_number,
                                  section.section_id,
                                  section.term.quarter,
                                  section.term.year)


def get_section_id(url):
    return re.sub(section_id_ext_pattern, r'\1',
                  url, flags=re.IGNORECASE)


def get_all_secondary_section_lists(primary_section):
    secondaries = []
    if primary_section.linked_section_urls and\
            len(primary_section.linked_section_urls):
        threads_dict = {}
        for url in primary_section.linked_section_urls:
            section_id = get_section_id(url)
            thread = ThreadWithResponse(target=get_single_course_list,
                                        args=(primary_section.curriculum_abbr,
                                              primary_section.course_number,
                                              section_id,
                                              primary_section.term.quarter,
                                              primary_section.term.year))
            thread.start()
            threads_dict[section_id] = thread

        for section_id in sorted(threads_dict.keys()):
            thread = threads_dict[section_id]
            thread.join()
            if thread.exception is None:
                secondaries.append(thread.response)
            else:
                logger.error("get_single_course_list(%s,%s,%s,%s,%s)==>%s ",
                             primary_section.curriculum_abbr,
                             primary_section.course_number,
                             section_id,
                             primary_section.term.quarter,
                             primary_section.term.year,
                             thread.exception)
    return secondaries


def get_course_email_lists(year, quarter, curriculum_abbr, course_number,
                           section_id, include_secondaries_in_primary):
    return get_section_email_lists(
        get_section_by_label(
            get_section_label(curriculum_abbr, course_number,
                              section_id, quarter, year)),
        include_secondaries_in_primary)


def get_section_email_lists(section,
                            include_secondaries_in_primary):
    """
    @param section: a valid sws.Section object
    """
    is_primary_section = section.is_primary_section
    json_data = {
        "year": section.term.year,
        "quarter": section.term.quarter,
        "course_abbr": section.curriculum_abbr,
        "course_number": section.course_number,
        "section_id": section.section_id,
        "is_primary": is_primary_section,
        "has_multiple_sections": False,
        "total_course_wo_list": 0,
        }
    json_data["section_list"] = get_single_section_list(section)

    if not json_data["section_list"]["list_exists"]:
        json_data["total_course_wo_list"] = 1

    if not is_primary_section:
        json_data["no_secondary_section"] = True
    else:
        total_secondaries = len(section.linked_section_urls)
        json_data["no_secondary_section"] = (total_secondaries == 0)

        if total_secondaries > 0:
            json_data["has_multiple_sections"] = True
            if include_secondaries_in_primary:
                secondary_lists = get_all_secondary_section_lists(section)

                json_data["secondary_section_lists"] = secondary_lists

                total_wo_list = get_total_course_wo_list(secondary_lists)
                json_data["total_course_wo_list"] += total_wo_list

                json_data["has_secondary_lists"] = \
                    (total_secondaries > total_wo_list)

                if total_secondaries > 1:
                    json_data["secondary_combined_list"] =\
                        get_section_secondary_combined_list(section)
    return json_data


def get_total_course_wo_list(secondary_section_lists):
    total = 0
    for section in secondary_section_lists:
        if not section["list_exists"]:
            total = total + 1
    return total


EMAIL_SUBJECT = 'instructor Mailman request'


def request_mailman_lists(requestor_uwnetid,
                          single_section_labels):
    """
    Required settings:
      EMAIL_HOST
      EMAIL_PORT
      MAILMAN_COURSEREQUEST_RECIPIENT
    """
    message_body, num_sections_found = get_message_body(
        requestor_uwnetid, single_section_labels)

    ret_data = {"total_lists_requested": num_sections_found}

    if num_sections_found == 0:
        ret_data["request_sent"] = False
    else:
        recipient = getattr(settings,
                            'MAILMAN_COURSEREQUEST_RECIPIENT',
                            None)
        if recipient is None:
            raise CourseRequestEmailRecipientNotFound
        sender = "%s@uw.edu" % requestor_uwnetid
        send_mail(EMAIL_SUBJECT,
                  message_body,
                  sender,
                  [recipient],
                  fail_silently=False)
        ret_data["request_sent"] = True
        logger.info("Request_mailman_lists: %s, message body: %s",
                    ret_data, message_body)

    return ret_data


def get_message_body(requestor_uwnetid,
                     single_section_labels):
    """
    subject: "instructor Mailman request"
    message body:
    <requestor_netid>
    <list_address> <quarter_code> YYYY <sln>
    <list_address> <quarter_code> YYYY <sln>
    """
    message_body = "%s\n" % requestor_uwnetid
    num_sections_found = 0

    threads = []
    for section_label in single_section_labels:
        thread = ThreadWithResponse(target=get_section_by_label,
                                    args=(section_label,))
        thread.start()
        threads.append(thread)

    for thrd in threads:
        thrd.join()
        if thrd.exception is None:
            section = thrd.response
            num_sections_found += 1
            message_body += _get_single_line(section)
        else:
            logger.error("%s", thread.exception)

    return message_body, num_sections_found


def _get_single_line(section):
    """
    <list_address> <quarter_code> YYYY <sln>
    """
    return "%s %s %s %s\n" % (
            get_section_list_name(section),
            _get_quarter_code(section.term.quarter),
            section.term.year,
            section.sln)


QUARTER_CODES = {
    "winter": 1,
    "spring": 2,
    "summer": 3,
    "autumn": 4,
}


def _get_quarter_code(quarter):
    return QUARTER_CODES[quarter.lower()]
