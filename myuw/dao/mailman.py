"""
Instructor class mailing list requests
"""

import logging
import re
from django.core.mail import send_mail
from uw_sws.section import get_section_by_label,\
    is_valid_section_label
from uw_mailman.basic_list import get_admin_url
from uw_mailman.course_list import get_course_list_name,\
    exists_course_list, get_section_secondary_combined_list_name,\
    exists_section_secondary_combined_list, get_section_list_name
from uw_mailman.instructor_term_list import\
    get_instructor_term_list_name, exists_instructor_term_list
from myuw.util.thread import ThreadWithResponse
from myuw.util.settings import get_mailman_courserequest_recipient
from myuw.logger.logresp import log_info
from myuw.dao import get_netid_of_current_user, get_userids
from myuw.dao.exceptions import CourseRequestEmailRecipientNotFound
from uw_sws.section import get_joint_sections


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
    return "{},{},{},{}/{}".format(year, quarter.lower(),
                                   curriculum_abbr, course_number, section_id)


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


def get_joint_course_list(curriculum_abbr, course_number, section_id,
                          quarter, year):
    exists = exists_course_list(curriculum_abbr, course_number,
                                section_id, quarter, year, True)

    data = get_list_json(
        exists, get_course_list_name(curriculum_abbr, course_number,
                                     section_id, quarter, year, True))
    data["section_id"] = section_id
    data["section_label"] = get_section_label(
        curriculum_abbr, course_number, section_id, quarter, year)
    return data


def get_joint_section_list(section):
    """
    @return json of the joint section email list info
    """
    return get_joint_course_list(section.curriculum_abbr,
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
                logger.error(
                    "{}. get_single_course_list({},{},{},{},{})==>{}".format(
                        get_userids(),
                        primary_section.curriculum_abbr,
                        primary_section.course_number,
                        section_id,
                        primary_section.term.quarter,
                        primary_section.term.year,
                        str(thread.exception)))
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

    if len(section.joint_section_urls):
        joint_sections = get_joint_sections(section)
        json_data['joint_sections'] = []
        json_data['has_joint'] = True
        json_data["joint_section_list"] = get_joint_section_list(section)
        for joint_section in joint_sections:
            joint_list = get_joint_section_list(joint_section)
            if joint_list['list_exists']:
                json_data["joint_section_list"] = joint_list
            joint_course = {
                "course_abbr": joint_section.curriculum_abbr,
                "course_number": joint_section.course_number,
                "section_id": joint_section.section_id,
                "course_abbr_slug":
                    joint_section.curriculum_abbr.replace(" ", "-")
            }
            json_data['joint_sections'].append(joint_course)

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
    json_data["has_lists"] = (json_data.get("has_secondary_lists") or
                              json_data["section_list"]["list_exists"])
    return json_data


def get_total_course_wo_list(secondary_section_lists):
    total = 0
    for section in secondary_section_lists:
        if not section["list_exists"]:
            total = total + 1
    return total


EMAIL_SUBJECT = 'instructor Mailman request'


def request_mailman_lists(request,
                          single_section_labels,
                          joint_section_lables):
    """
    Required settings:
      EMAIL_HOST
      EMAIL_PORT
      MAILMAN_COURSEREQUEST_RECIPIENT
    """
    requestor_uwnetid = get_netid_of_current_user(request)
    single_message_body, num_sections_found = get_single_message_body(
        requestor_uwnetid, single_section_labels)
    joint_message_body, joint_num_sections_found = \
        get_joint_message_body(requestor_uwnetid, joint_section_lables)

    message_body = None
    if single_message_body.count("\n") > 1:
        message_body = single_message_body
    if joint_message_body.count("\n") > 1:
        # remove first netid line if both single and joint requests are made
        if message_body is not None:
            message_body += joint_message_body.split("\n")[1:]
        else:
            message_body = joint_message_body

    ret_data = {"total_lists_requested":
                num_sections_found + joint_num_sections_found}
    if num_sections_found + joint_num_sections_found == 0:
        ret_data["request_sent"] = False
    else:
        recipient = get_mailman_courserequest_recipient()
        if recipient is None:
            raise CourseRequestEmailRecipientNotFound
        sender = "{}@uw.edu".format(requestor_uwnetid)
        send_mail(EMAIL_SUBJECT,
                  message_body,
                  sender,
                  [recipient],
                  fail_silently=False)
        ret_data["request_sent"] = True
    return ret_data


def get_single_message_body(requestor_uwnetid,
                            single_section_labels):
    """
    subject: "instructor Mailman request"
    message body:
    <requestor_netid>
    <list_address> <quarter_code> YYYY <sln>
    <list_address> <quarter_code> YYYY <sln>
    """
    message_body = "{}\n".format(requestor_uwnetid)
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
            logger.error(
                "{}. get_single_message_body ==> {}".format(
                    get_userids(), str(thread.exception)))
    log_info(logger, "For {} ==request emaillist message body==> {}".format(
        single_section_labels, message_body.splitlines()))
    return message_body, num_sections_found


def get_joint_message_body(requestor_uwnetid, joint_section_labels):
    """
    subject: "instructor Mailman request"
    message body:
    <requestor_netid>
    <joint_list_address> <quarter_code> YYYY <sln1>
    <joint_list_address> <quarter_code> YYYY <sln2>
    """
    message_body = "{}\n".format(requestor_uwnetid)
    num_sections_found = 0

    threads = []
    for section_label in joint_section_labels:
        thread = ThreadWithResponse(target=get_section_by_label,
                                    args=(section_label,))
        thread.start()
        threads.append(thread)

    for thrd in threads:
        thrd.join()
        if thrd.exception is None:
            section = thrd.response
            num_sections_found += 1
            message_body += _get_joint_line(section)
        else:
            logger.error("{}. get_joint_message_body ==> {}".format(
                get_userids(), str(thread.exception)))
    log_info(logger, "For {} ==request emaillist message body==> {}".format(
        joint_section_labels, message_body.splitlines()))
    return message_body, num_sections_found


def _get_single_line(section):
    """
    <list_address> <quarter_code> YYYY <sln>
    """
    return "{} {} {} {}\n".format(get_section_list_name(section),
                                  _get_quarter_code(section.term.quarter),
                                  section.term.year,
                                  section.sln)


def _get_joint_line(section):
    """
    <list_address> <quarter_code> YYYY <sln>
    """
    joint_slns = [section.sln]
    for section in get_joint_sections(section):
        joint_slns.append(section.sln)

    sln_string = " ".join(map(str, joint_slns))
    return "{} {} {} {}\n".format(
        get_course_list_name(section.curriculum_abbr,
                             section.course_number,
                             section.section_id,
                             section.term.quarter,
                             section.term.year,
                             True),
        _get_quarter_code(section.term.quarter),
        section.term.year,
        sln_string)


QUARTER_CODES = {
    "winter": 1,
    "spring": 2,
    "summer": 3,
    "autumn": 4,
}


def _get_quarter_code(quarter):
    return QUARTER_CODES[quarter.lower()]
