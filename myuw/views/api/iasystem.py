# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import time
import traceback
from operator import itemgetter
from myuw.dao import get_netid_of_current_user
from myuw.dao.pws import is_student
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.iasystem import (
    get_evaluations_by_section, json_for_evaluation, in_coursevel_fetch_window)
from myuw.logger.logresp import (
    log_data_not_found_response, log_msg, log_api_call)
from myuw.logger.timer import Timer
from myuw.views import prefetch_resources
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, handle_exception


logger = logging.getLogger(__name__)
MOCKDAO = 'restclients.dao_implementation.iasystem.File'


class IASystem(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/ias/*.
    """
    def get(self, request, *args, **kwargs):
        """
        GET /api/v1/ias/
        """
        timer = Timer()
        try:
            prefetch_resources(request)

            # time.sleep(10)
            if not is_student(request):
                log_msg(logger, timer, "Not a student, abort!")
                return data_not_found()

            if not in_coursevel_fetch_window(request):
                # The window starts: 7 days before last inst
                # ends: the midnight at the end of current term
                # grade submission deadline
                log_msg(logger, timer, "Not in fetching window")
                return data_not_found()

            schedule = get_schedule_by_term(request)
            if len(schedule.sections) == 0:
                log_data_not_found_response(logger, timer)
                return data_not_found()

            resp_data = load_course_eval(request, schedule)
            log_api_call(timer, request, "Get IASystem")
            return self.json_response(resp_data)
        except Exception:
            return handle_exception(logger, timer, traceback)


def load_course_eval(request, schedule):
    """
    @return the course schedule sections having
    the attribute ["evaluation_data"] with the evaluations
    that should be shown; or
    "{}" if wouldn't display any; or
    None if a data error.
    """
    json_data = schedule.json_data()
    if schedule.term.is_summer_quarter():
        json_data["summer_term"] = schedule.summer_term

    section_index = 0
    for section in schedule.sections:
        section_data = json_data["sections"][section_index]
        section_index += 1
        try:
            section_data["evaluation_data"] = json_for_evaluation(
                request, get_evaluations_by_section(request, section), section)
        except Exception as ex:
            section_data["evaluation_data"] = None

    json_data["sections"] = sorted(json_data["sections"],
                                   key=itemgetter('curriculum_abbr',
                                                  'course_number',
                                                  'section_id'))
    return json_data
