import logging
import traceback
from myuw.dao.enrollment import get_prev_enrollments_with_open_sections
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.term import get_previous_number_quarters
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call, log_data_not_found_response
from myuw.views import prefetch_resources
from myuw.views.api.base_schedule import StudClasSche, load_schedule
from myuw.views.error import handle_exception, data_not_found

logger = logging.getLogger(__name__)


class StudUnfinishedPrevQuarClasSche(StudClasSche):
    """
    Performs actions on resource at
    /api/v1/schedule/prev_unfinished
    """
    def get(self, request, *args, **kwargs):
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
            prefetch_resources(request)
            enrollment_dict = get_prev_enrollments_with_open_sections(
                request, 2)
            has_unfinished_course = False
            for term in enrollment_dict.keys():
                term_enrollments = enrollment_dict[term]
                if term_enrollments.has_unfinished_pce_course():
                    has_unfinished_course = True
                    break

            if not has_unfinished_course:
                log_data_not_found_response(logger, timer)
                return data_not_found()

            resp_data = self.make_resp_json(request, enrollment_dict)
            log_api_call(timer, request,
                         "Get StudUnfinishedPrevQuarClasSche")
            return self.json_response(resp_data)
        except Exception:
            return handle_exception(logger, timer, traceback)

    def make_resp_json(self, request, enrollment_dict):
        ret_json = []
        terms = get_previous_number_quarters(request, 2)

        for term in terms:
            if term in enrollment_dict:
                term_enrollments = enrollment_dict[term]

                if term_enrollments.has_unfinished_pce_course():
                    schedule_json = self.get_term_schedule(
                        request, term, term_enrollments.unf_pce_courses)
                    ret_json.append(schedule_json)
        return ret_json

    def get_term_schedule(self, request, term, unfinished_sections):
        """
        Return only unfinished course schedule
        """
        schedule = get_schedule_by_term(
            request, term=term, summer_term='full-term')
        include_sections = []
        for section in schedule.sections:
            if section.section_label() in unfinished_sections:
                include_sections.append(section)
        # replace schedule.sections with only unfinished sections
        schedule.sections = include_sections
        return load_schedule(request, schedule)
