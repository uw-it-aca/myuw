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
from myuw.dao.mailman import get_course_email_lists, request_mailman_lists
from myuw.views.error import handle_exception, not_instructor_error


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
        if re.match(r'^section_single_', key) or\
                re.match(r'^secondary_single_', key):
            single_section_labels.append(request.POST[key])
    return single_section_labels
