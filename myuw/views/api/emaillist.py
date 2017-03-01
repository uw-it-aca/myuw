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
from myuw.dao.instructor_schedule import is_instructor, is_section_instructor
from myuw.dao.user import get_netid_of_current_user
from myuw.dao.mailman import get_course_email_lists, request_mailman_lists,\
    is_valid_section_label
from myuw.views.error import handle_exception, not_instructor_error,\
    InvalidInputFormData


logger = logging.getLogger(__name__)


class Emaillist(RESTDispatch):

    def GET(self, request, year, quarter,
            curriculum_abbr, course_number, section_id):
        print "GET"
        """
        GET returns 200 with email lists for the course
        """
        timer = Timer()
        try:
            section_label = "%s,%s,%s,%s/%s" % (year,
                                                quarter.lower(),
                                                curriculum_abbr.upper(),
                                                course_number,
                                                section_id)
            if not is_section_instructor(section_label):
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
        print "POST"
        try:
            print 2
            single_section_labels = get_input(request)
            print 3
            if not validate_is_instructor(single_section_labels):
                logger.error("%s is not an instructor",
                             get_netid_of_current_user())
                return not_instructor_error()

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
    print "2.5"
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
            print "2.52"
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


def validate_is_instructor(section_labels):
    """
    returns true if user is instructor of **all** labels
    """
    print 'v'
    for section_label in section_labels:
        if is_section_instructor(section_label) is False:
            return False
    return True
