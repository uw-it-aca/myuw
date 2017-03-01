import json
import traceback
import logging
import re
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response
from myuw.views.rest_dispatch import RESTDispatch
from myuw.dao.instructor_schedule import is_instructor
from myuw.dao.user import get_netid_of_current_user
from myuw.dao.mailman import get_course_email_lists,\
    request_mailman_lists, get_sections_wo_email_lists,\
    is_valid_section_label
from myuw.views.error import handle_exception, not_instructor_error,\
    InvalidInputFormData


logger = logging.getLogger(__name__)


class Emaillist(RESTDispatch):

    def GET(self, request, year, quarter,
            curriculum_abbr, course_number, section_id):
        """
        GET returns 200 with email lists for the course
        """
        timer = Timer()
        try:
            if not is_instructor(request):
                return not_instructor_error()

            email_list_json = get_course_email_lists(
                year, quarter, curriculum_abbr,
                course_number, section_id, True)

            log_success_response(logger, timer)
            return HttpResponse(json.dumps(email_list_json))
        except Exception:
            return handle_exception(logger, timer, traceback)

    @method_decorator(csrf_protect)
    def POST(self, request):
        timer = Timer()
        try:
            if not is_instructor(request):
                logger.error("%s is not an instructor",
                             get_netid_of_current_user())
                return not_instructor_error()

            single_section_labels = get_input(request)
            if len(single_section_labels) == 0:
                resp = {"none_selected": True}
            else:
                resp = request_mailman_lists(get_netid_of_current_user(),
                                             single_section_labels)
                log_success_response(logger, timer)

            return HttpResponse(json.dumps(resp))
        except Exception:
            return handle_exception(logger, timer, traceback)


def get_input(request):
    single_section_labels = []
    for key in request.POST:
        if re.match(r'^[a-z]+_single_[A-Z][A-Z0-9]?$', key):
            section_label = request.POST[key]

            if section_id_matched(key, section_label) and\
                    is_valid_section_label(section_label):
                single_section_labels.append(request.POST[key])
                continue

            logger.error("Invalid section label (%s) in the form input",
                         section_label)
            raise InvalidInputFormData
    return single_section_labels


SINGLE_SECTION_SELECTION_KEY_PATTERN = r'^[a-z]+_single_([A-Z][A-Z0-9]?)$'


def section_id_matched(key, value):
    """
    key and value Strings
    """
    try:
        section_id = re.sub(SINGLE_SECTION_SELECTION_KEY_PATTERN,
                            r'\1',
                            key,
                            flags=re.IGNORECASE)
        section_label_pattern = (r"^\d{4},[a-z]+,[ &A-Z]+,\d+/" +
                                 section_id + "$")
        return re.match(section_label_pattern, value,
                        flags=re.IGNORECASE) is not None
    except TypeError:
        return False
