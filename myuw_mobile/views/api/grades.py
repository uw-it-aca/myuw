from django.http import HttpResponse
from django.utils import simplejson as json
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.sws import Quarter, Schedule
from operator import itemgetter


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
        json_data = schedule.json_data()

        section_index = 0
        for section in schedule.sections:
            section_data = json_data["sections"][section_index]
            color = colors[section.section_label()]
            section_data["color_id"] = color

            # XXX - Fake Data!
            section_data["official_grade"] = "3.8"
            section_data["assignments"] = [
                    {
                        "source_id": "catalyst_gradebook",
                        "source_name": "Catalyst GradeBook",
                        "data": [ {
                            "class_grade": "3.9",
                            "total_score": 87,
                            "url": "https://catalyst.uw.edu/gradebook/owner/id",
                            "name": "Gradebook for the course",
                            "assignments": [
                                { "name": "Homework 1", "score": 90, "type": "points", "max_points": 100 },
                                { "name": "Homework 2", "score": 95, "type": "percentage" },
                                { "name": "Homework 3", "score": "2.7", "type": "grade_point" },
                                { "name": "Homework 4", "score": "B", "type": "custom" },
                                { "name": "Homework 5", "score": "nice", "type": "text" }
                            ]
                        } ]
                    },
                    {
                        "source_id": "catalyst_webq",
                        "source_name": "Catalyst WebQ",
                        "data": [ {
                            "assignments": [
                                { "name": "Quiz 1", "score": 4, "type": "points", "max_points": 5, "url": "https://catalyst.uw.edu/webq/owner/id/" }
                            ]
                        } ]
                    }
                ]

            section_index += 1

        json_data["sections"] = sorted(json_data["sections"],
                                   key=itemgetter('curriculum_abbr',
                                                  'course_number',
                                                  'section_id',
                                                  ))


        return HttpResponse(json.dumps(json_data), { "Content-Type": "application/json" })
