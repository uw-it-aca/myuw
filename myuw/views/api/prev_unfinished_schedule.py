import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.enrollment import get_prev_enrollments_with_open_sections
from myuw.dao.schedule import get_schedule_by_term
from myuw.dao.term import get_prev_num_terms
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg, log_success_response,\
    log_data_not_found_response
from myuw.views.api.base_schedule import StudClasSche, load_schedule
from myuw.views.error import handle_exception, data_not_found


logger = logging.getLogger(__name__)


class StudUnfinishedPrevQuarClasSche(StudClasSche):
    """
    Performs actions on resource at
    /api/v1/schedule/prev_unfinished
    """
    def GET(self, request):
        """
        GET returns 200 with course section schedule details of
        the unfinished previous quarters' PCE course
        Return the course sections of full term and matched term
        if a specific summer-term is given
        @return class schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        try:
            enrollment_dict = get_prev_enrollments_with_open_sections(
                request, 2)
            has_unfinished_course = False
            for term in enrollment_dict.keys():
                term_enrollments = enrollment_dict[term]
                if term_enrollments.has_off_term_course():
                    has_unfinished_course = True
                    break

            if not has_unfinished_course:
                log_data_not_found_response(logger, timer)
                return data_not_found()

            resp_data = self.make_resp_json(request, enrollment_dict)
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(resp_data))
        except Exception:
            return handle_exception(logger, timer, traceback)

    def make_resp_json(self, request, enrollment_dict):
        ret_json = []
        terms = get_prev_num_terms(request, 2)

        for term in reversed(terms):
            if term in enrollment_dict:
                term_enrollments = enrollment_dict[term]

                if term_enrollments.has_off_term_course():
                    schedule_json = self.get_term_schedule(
                        request, term, term_enrollments.off_term_sections)
                    ret_json.append(schedule_json)
        return ret_json

    def get_term_schedule(self, request, term, unfinished_sections):
        schedule = get_schedule_by_term(request, term)
        include_sections = []
        for section in schedule.sections:
            if section.section_label() in unfinished_sections:
                include_sections.append(section)
        # replace schedule.sections with only unfinished sections
        schedule.sections = include_sections
        return load_schedule(request, schedule)
