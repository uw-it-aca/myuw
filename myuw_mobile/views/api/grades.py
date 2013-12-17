from django.http import HttpResponse
from django.utils import simplejson as json
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.sws import Quarter, Schedule
from restclients.catalyst.gradebook import GradeBook
from restclients.catalyst.webq import WebQ
from operator import itemgetter
from myuw_mobile.user import UserService


class Grades(RESTDispatch):
    """
    Handles /api/v1/grades/
    """
    def GET(self, request, year=None, quarter=None):
        """
        Returns grades for a given term.  If no term is given, the current
        term is used.
        """
        schedule_dao = Schedule()
        quarter_dao = Quarter()

        if year and quarter:
            term = quarter_dao.get_term(year, quarter.lower())
        else:
            term = quarter_dao.get_cur_quarter()

        if term is not None:
            schedule = schedule_dao.get_schedule(term)

        if schedule is None or not schedule.json_data():
            log_data_not_found_response(logger, timer)
            return HttpResponse({})

        colors = schedule_dao.get_colors_for_schedule(schedule)
        grades = self._get_grades_for_term(term.year, term.quarter)

        json_data = schedule.json_data()

        section_index = 0
        for section in schedule.sections:
            section_data = json_data["sections"][section_index]
            color = colors[section.section_label()]

            section_data["color_id"] = color

            self._add_grades_for_section(grades, section_data, section.section_label())

            # XXX - Fake Data!
            section_data["official_grade"] = "3.8"

            section_index += 1

        json_data["sections"] = sorted(json_data["sections"],
                                   key=itemgetter('curriculum_abbr',
                                                  'course_number',
                                                  'section_id',
                                                  ))


        return HttpResponse(json.dumps(json_data), { "Content-Type": "application/json" })

    def _get_grades_for_term(self, year, quarter):
        # XXX -Thread these methods!
        netid = UserService().get_user()
        gradebook_grades = GradeBook().get_grades_for_student_and_term(netid, year, quarter)
        webq_grades = WebQ().get_grades_for_student_and_term(netid, year, quarter)

        return { "catalyst_gradebook": gradebook_grades, "catalyst_webq": webq_grades  }

    def _add_grades_for_section(self, all_grades, section_data, section_label):
        self._add_grades(all_grades["catalyst_gradebook"], section_data, section_label, "catalyst_gradebook", "Catalyst GradeBook")
        self._add_grades(all_grades["catalyst_webq"], section_data, section_label, "catalyst_webq", "Catalyst WebQ")

    def _add_grades(self, source_data, section_data, section_label, source_key, source_name):
        if section_label in source_data:
            section_grades = source_data[section_label]

            data = []

            for grades in section_grades:
                data.append(grades.json_data())

            if not "assignments" in section_data:
                section_data["assignments"] = []

            section_data["assignments"].append({
                "source_id": source_key,
                "source_name": source_name,
                "data": data
            })

