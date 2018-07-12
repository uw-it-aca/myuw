import traceback
import logging
import re
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from restclients_core.exceptions import DataFailureException
from uw_sws.exceptions import InvalidSectionID
from myuw.dao import get_netid_of_current_user, is_action_disabled
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.instructor_schedule import check_section_instructor
from myuw.dao.mailman import (
    get_course_email_lists, request_mailman_lists, is_valid_section_label,
    get_section_by_label)
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg_with_request
from myuw.views.api import ProtectedAPI
from myuw.views.exceptions import DisabledAction, NotInstructorError,\
    InvalidInputFormData
from myuw.views.error import handle_exception
from uw_sws.section import get_section_by_label
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
            section_label = "%s,%s,%s,%s/%s" % (year,
                                                quarter.lower(),
                                                cur_abb.upper(),
                                                course_number,
                                                section_id)

            if not is_emaillist_authorized(request, section_label):
                raise NotInstructorError(
                    "Not an instructor when checking emaillist for %s" %
                    section_label)

            email_list_json = get_course_email_lists(
                year, quarter, cur_abb, course_number, section_id, True)
            log_msg_with_request(logger, timer, request,
                                 "Checked emaillist for %s" % section_label)
            return self.json_response(email_list_json)
        except Exception:
            return handle_exception(logger, timer, traceback)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        timer = Timer()
        try:
            section_labels = get_input(request)
            if len(section_labels) == 0:
                resp = {"none_selected": True}
            else:

                if is_action_disabled():
                    raise DisabledAction(
                        "Request emaillist w. Overriding for %s" %
                        section_labels)

                if not validate_is_instructor(request, section_labels):
                    raise NotInstructorError(
                        "Not an instructor when requesting emaillist for %s" %
                        section_labels)

                resp = request_mailman_lists(request, section_labels)

            log_msg_with_request(logger, timer, request,
                                 "Request emaillist for %s ==> %s" % (
                                     section_labels, resp))

            return self.json_response(resp)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)


def get_input(request):
    section_labels = []
    for key in request.POST:
        if re.match(r'^[a-z]+_single_[A-Z][A-Z0-9]?$', key) or \
                re.match(r'^[a-z]+_joint_[A-Z][A-Z0-9]?$', key):
            section_label = request.POST[key]

            if section_id_matched(key, section_label) and \
                    is_valid_section_label(section_label):
                section_labels.append(request.POST[key])
                continue

            logger.error("Invalid section label (%s) in the form input",
                         section_label)
            raise InvalidInputFormData
    return section_labels


SINGLE_SECTION_SELECTION_KEY_PATTERN = r'^[a-z]+_single_([A-Z][A-Z0-9]?)$'
JOINT_SECTION_SELECTION_KEY_PATTERN = r'^[a-z]+_joint_([A-Z][A-Z0-9]?)$'


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


def validate_is_instructor(request, section_labels):
    """
    returns true if user is instructor/authorized submitter of **all** labels
    """
    for section_label in section_labels:
        if is_emaillist_authorized(request, section_label) is False:
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
        logger.error("%s is_emaillist_authorized(%s) ==> InvalidSectionLabel",
                     uwnetid, section_label)
        return False
    except NotSectionInstructorException:
        logger.error("%s is_emaillist_authorized(%s) ==> NotSectionInstructor",
                     uwnetid, section_label)
        return False
    except DataFailureException as err:
        if err.status == 404:
            return False
        raise
    except Exception as ex:
        raise
