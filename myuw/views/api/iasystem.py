import json
import logging
import time
import traceback
from operator import itemgetter
from django.conf import settings
from django.http import HttpResponse
from myuw.dao.gws import is_student
from myuw.dao.pws import get_netid_of_current_user
from myuw.dao.schedule import get_schedule_by_term
from myuw.dao.schedule import filter_schedule_sections_by_summer_term
from myuw.dao.registered_term import get_current_summer_term_in_schedule
from myuw.dao.term import get_comparison_date, get_current_quarter
from myuw.dao.iasystem import get_evaluations_by_section,\
    json_for_evaluation, in_coursevel_fetch_window
from myuw.logger.logresp import log_data_not_found_response,\
    log_msg, log_success_response
from myuw.logger.timer import Timer
from myuw.views.rest_dispatch import RESTDispatch, data_not_found,\
    handle_exception


logger = logging.getLogger(__name__)
MOCKDAO = 'restclients.dao_implementation.iasystem.File'


class IASystem(RESTDispatch):
    """
    Performs actions on resource at /api/v1/ias/*.
    """

    def GET(self, request):
        """
        GET /api/v1/ias/
        """
        timer = Timer()
        try:
            dao_class = getattr(settings,
                                "RESTCLIENTS_IASYSTEM_DAO_CLASS",
                                MOCKDAO)
            if dao_class == MOCKDAO and\
                    get_netid_of_current_user() == "eight":
                time.sleep(10)

            if not is_student():
                log_msg(logger, timer, "Not a student, abort!")
                return data_not_found()

            if not in_coursevel_fetch_window(request):
                # The window starts: 7 days before last inst
                # ends: the midnight at the end of current term
                # grade submission deadline
                log_msg(logger, timer, "Not in fetching window")
                return data_not_found()
            term = get_current_quarter(request)
            schedule = get_schedule_by_term(request, term)

            summer_term = get_current_summer_term_in_schedule(
                schedule, request)

            filter_schedule_sections_by_summer_term(schedule, summer_term)
            if len(schedule.sections) == 0:
                log_data_not_found_response(logger, time)
                return data_not_found()

            resp_data = load_course_eval(request, schedule, summer_term)
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(resp_data))
        except Exception:
            return handle_exception(logger, timer, traceback)


def load_course_eval(request, schedule, summer_term=""):
    """
    @return the course schedule sections having
    the attribute ["evaluation_data"] with the evaluations
    that should be shown; or
    "{}" if whouldn't display any; or
    None if a data error.
    """
    json_data = schedule.json_data()
    json_data["summer_term"] = summer_term

    section_index = 0
    for section in schedule.sections:
        section_data = json_data["sections"][section_index]
        section_index += 1
        try:
            section_data["evaluation_data"] = json_for_evaluation(
                request, get_evaluations_by_section(section), section)
        except Exception as ex:
            section_data["evaluation_data"] = None

    json_data["sections"] = sorted(json_data["sections"],
                                   key=itemgetter('curriculum_abbr',
                                                  'course_number',
                                                  'section_id'))
    return json_data
