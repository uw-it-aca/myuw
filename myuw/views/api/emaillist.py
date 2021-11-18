# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import traceback
import logging
import re
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from restclients_core.exceptions import DataFailureException
from uw_sws.section import get_section_by_label, get_joint_sections
from uw_sws.exceptions import InvalidSectionID
from myuw.dao import is_action_disabled
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.pws import get_person_of_current_user, is_employee
from myuw.dao.instructor_schedule import check_section_instructor
from myuw.dao.mailman import (
    get_course_email_lists, request_mailman_lists, is_valid_section_label,
    get_section_by_label)
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.exceptions import DisabledAction, NotInstructorError,\
    InvalidInputFormData
from myuw.views.error import handle_exception
from myuw.views.api import unescape_curriculum_abbr

logger = logging.getLogger(__name__)


class Emaillist(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with email lists for the course
        """
        timer = Timer()
        try:
            year = kwargs.get("year")
            quarter = kwargs.get("quarter")
            curriculum_abbr = kwargs.get("curriculum_abbr")
            course_number = kwargs.get("course_number")
            section_id = kwargs.get("section_id")
            cur_abb = unescape_curriculum_abbr(curriculum_abbr)
            section_label = "{},{},{},{}/{}".format(year,
                                                    quarter.lower(),
                                                    cur_abb.upper(),
                                                    course_number,
                                                    section_id)

            if not is_emaillist_authorized(request, section_label):
                raise NotInstructorError(
                    "Not instructor can't get emaillist for {}".format(
                        section_label))

            email_list_json = get_course_email_lists(
                year, quarter, cur_abb, course_number, section_id, True)
            log_api_call(timer, request,
                         "Get emaillist for {}".format(section_label))
            return self.json_response(email_list_json)
        except Exception:
            return handle_exception(logger, timer, traceback)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        timer = Timer()
        try:
            (single_section_labels, joint_section_labels) = get_input(request)
            if len(single_section_labels) == 0 == len(joint_section_labels):
                resp = {"none_selected": True}
            else:

                if is_action_disabled():
                    raise DisabledAction(
                        "Overriding can't request emaillist for "
                        "single :{} and joint:{}".format(
                            single_section_labels,
                            joint_section_labels))

                if (not is_employee(request) or
                        not validate_is_instructor(
                            request,
                            single_section_labels,
                            joint_section_labels)):
                    raise NotInstructorError(
                        "Not a current instructor can't request emaillist for"
                        "single :{} and joint:{}".format(
                            single_section_labels,
                            joint_section_labels))

                resp = request_mailman_lists(request,
                                             single_section_labels,
                                             joint_section_labels)

            log_api_call(timer, request,
                         "Create/Request emaillist for {}, {} ==> {}".format(
                             single_section_labels,
                             joint_section_labels,
                             resp))

            return self.json_response(resp)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)


def get_input(request):
    single_section_labels = []
    joint_section_labels = []
    if "section_joint_list" in request.POST and \
            request.POST["section_joint_list"] == "joint":
        for key in request.POST:
            if re.match(r'^[a-z]+_id_[A-Z][A-Z0-9]?$', key):
                joint_section_labels.append(
                    _get_section_label(request, key))

    else:
        for key in request.POST:
            if re.match(r'^[a-z]+_single_[A-Z][A-Z0-9]?$', key) or \
                    re.match(r'^[a-z]+_id_[A-Z][A-Z0-9]?$', key):
                single_section_labels.append(_get_section_label(request, key))

    return single_section_labels, joint_section_labels


def _get_section_label(request, key):
    section_label = request.POST[key]
    if section_id_matched(key, section_label) and \
            is_valid_section_label(section_label):
        return section_label
    raise InvalidInputFormData(
        "Invalid section label ({}) in emaillist form input".format(
            section_label))


SINGLE_SECTION_SELECTION_KEY_PATTERN = r'^[a-z]+_single_([A-Z][A-Z0-9]?)$'
JOINT_SECTION_SELECTION_KEY_PATTERN = r'^[a-z]+_id_([A-Z][A-Z0-9]?)$'


def section_id_matched(key, value):
    """
    key and value Strings
    """
    try:
        (section_id, sub_count) = re.subn(SINGLE_SECTION_SELECTION_KEY_PATTERN,
                                          r'\1',
                                          key,
                                          flags=re.IGNORECASE)
        if sub_count == 0:
            section_id = re.sub(JOINT_SECTION_SELECTION_KEY_PATTERN,
                                r'\1',
                                key,
                                flags=re.IGNORECASE)
        section_label_pattern = (r"^\d{4},[a-z]+,[ &A-Z]+,\d+/" +
                                 section_id + "$")
        return re.match(section_label_pattern, value,
                        flags=re.IGNORECASE) is not None
    except TypeError:
        return False


def validate_is_instructor(request, single_section_labels,
                           joint_section_labels):
    """
    returns true if user is instructor/authorized submitter of **all** labels
    """
    for section_label in single_section_labels:
        if is_emaillist_authorized(request, section_label) is False:
            return False
    for section_label in joint_section_labels:
        if is_joint_emaillist_authorized(request, section_label) is False:
            return False
    return True


def is_emaillist_authorized(request, section_label):
    """
    Determines if user is authorized to create mailing lists for that section:
    Instructor of section OR instructor of primary section
    """
    person = get_person_of_current_user(request)
    uwnetid = person.uwnetid
    try:
        check_section_instructor(get_section_by_label(section_label), person)
        return True
    except InvalidSectionID:
        logger.error("{} is_emaillist_authorized({}) InvalidSectionID".format(
                     uwnetid, section_label))
        return False
    except NotSectionInstructorException:
        logger.error(
            "{} is_emaillist_authorized({}) ==> NotSectionInstructor".format(
                uwnetid, section_label))
        return False
    except DataFailureException as err:
        if err.status == 404:
            return False
        raise
    except Exception as ex:
        raise


def is_joint_emaillist_authorized(request, section_label):
    """
    Determines if user is authorized to create mailing lists for that section:
    Instructor of section OR instructor of primary section
    """
    person = get_person_of_current_user(request)
    uwnetid = person.uwnetid
    section = get_section_by_label(section_label)
    try:
        check_section_instructor(section, person)
        return True
    except InvalidSectionID:
        logger.error(
            "{} is_joint_emaillist_authorized({}) InvalidSectionID".format(
                uwnetid, section_label))
        return False
    except NotSectionInstructorException:
        if len(section.joint_section_urls):
            joint_sections = get_joint_sections(section)
            is_joint_instructor = False
            for joint_section in joint_sections:
                try:
                    check_section_instructor(joint_sections, person)
                    is_joint_instructor = True
                except NotSectionInstructorException:
                    pass
            if is_joint_instructor:
                return True
    except DataFailureException as err:
        if err.status == 404:
            return False
        raise
    except Exception as ex:
        raise
