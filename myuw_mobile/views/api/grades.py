from operator import itemgetter
from django.http import HttpResponse
import json
from userservice.user import UserService
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.course_color import get_colors_by_schedule
from myuw_mobile.dao.final_grade import get_grades_by_term
from myuw_mobile.dao.schedule import get_schedule_by_term
from myuw_mobile.dao.term import get_quarter
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response
from myuw_mobile.logger.logresp import log_success_response
import logging


class Grades(RESTDispatch):
    """
    Handles /api/v1/grades/
    """
    def GET(self, request, year=None, quarter=None):
        """
        Returns grades for a given term.  If no term is given, the current
        term is used.
        """
        timer = Timer()
        logger = logging.getLogger(__name__)
        term = get_quarter(year, quarter)
        if term is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        schedule = get_schedule_by_term(term)
        if schedule is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        colors = get_colors_by_schedule(schedule)
        if colors is None and len(schedule.sections) > 0:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        grade_by_section_label = get_grades_by_term(term)

        json_data = schedule.json_data()

        section_index = 0
        for section in schedule.sections:
            section_label = section.section_label()
            section_data = json_data["sections"][section_index]
            color = colors[section_label]

            section_data["color_id"] = color

            if section_label in grade_by_section_label:
                grade_data = grade_by_section_label[section_label]
                section_data["official_grade"] = grade_data.grade

            section_index += 1

        json_data["sections"] = sorted(json_data["sections"],
                                       key=itemgetter('curriculum_abbr',
                                                      'course_number',
                                                      'section_id',
                                                      )
                                       )

        return HttpResponse(json.dumps(json_data),
                            {"Content-Type": "application/json"}
                            )

    def _add_grades(self, source_data, section_data, section_label,
                    source_key, source_name):
        if section_label in source_data:
            section_grades = source_data[section_label]

            data = []

            for grades in section_grades:
                data.append(grades.json_data())

            if "assignments" not in section_data:
                section_data["assignments"] = []

            section_data["assignments"].append({
                "source_id": source_key,
                "source_name": source_name,
                "data": data
            })
