from django.http import HttpResponse
from django.utils import simplejson as json
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.sws import Quarter, Schedule
from restclients.catalyst.gradebook import GradeBook
from restclients.catalyst.webq import WebQ
from restclients.sws import SWS
from restclients.pws import PWS
from restclients.canvas.quizzes import Quizzes
from restclients.canvas.submissions import Submissions
from restclients.canvas.assignments import Assignments
from restclients.canvas.enrollments import Enrollments
from restclients.canvas import Canvas
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

        username = UserService().get_user()
        regid = PWS().get_person_by_netid(username).uwregid

        grades = self._get_grades_for_term(term.year, term.quarter)
        canvas_grades = self._get_canvas_grades_for_schedule(schedule, regid)

        final_grades = SWS().grades_for_regid_and_term(regid, term)

        grade_by_section_label = {}
        for grade in final_grades.grades:
            grade_by_section_label[grade.section.section_label()] = grade

        json_data = schedule.json_data()

        section_index = 0
        for section in schedule.sections:
            section_label = section.section_label()
            section_data = json_data["sections"][section_index]
            color = colors[section_label]

            section_data["color_id"] = color

            self._add_grades_for_section(grades, section_data, section_label)
            self._add_canvas_grades_for_section(canvas_grades, section_data, section_label)

            if section_label in grade_by_section_label:
                grade_data = grade_by_section_label[section_label]
                section_data["official_grade"] = grade_data.grade

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
    def _get_canvas_grades_for_schedule(self, schedule, regid):
        canvas = Canvas()
        grades = {}
        for section in schedule.sections:
            grades[section.section_label()] = self._get_canvas_grades_section_sis_id(canvas.generate_section_id(section), regid)
        return grades
        
        
    def _get_canvas_grades_section_sis_id(self, section_sis_id, regid):
        sub_cli = Submissions(as_user=regid)
        submissions = []
        try:
            submissions = sub_cli.get_submissions_multiple_assignments_by_sis_id(False, section_sis_id)
        except:
            pass
        assign_cli = Assignments(as_user=regid)
        assignments = []
        try:
            assignments = assign_cli.get_assignments_by_sis_id(section_sis_id)
        except:
            pass
        quiz_cli = Quizzes(as_user=regid)
        quizzes = []
        try:
            quizzes = quiz_cli.get_quizzes_by_sis_id(section_sis_id)
        except:
            pass

        assignments_data = []
        submission_map = {}
        for submission in submissions:
            submission_map[submission.assignment_id] = submission
        for assignment in assignments:
            assign = {}
            assign['name'] = assignment.name
            assign['max_points'] = assignment.points_possible
            assign['url'] = assignment.html_url
            if assignment.assignment_id in submission_map:
                assign['score'] = submission_map[assignment.assignment_id].grade
            assignments_data.append(assign)
        
        quizzes_data = []
        for quiz in quizzes:
            quiz_data = {}
            quiz_data['name'] = quiz.title
            quiz_data['url'] = quiz.html_url
            if quiz.quiz_id in submission_map:
                quiz_data['score'] = submission_map[quiz.quiz_id].grade
            quizzes_data.append(quiz_data)

        return { "canvas_assignments": assignments_data, "canvas_quizzes": quizzes_data  }

    def _add_canvas_grades_for_section(self, canvas_grades, section_data, section_label):
        

        if not "assignments" in section_data:
            section_data["assignments"] = []

        section_data["assignments"].append({
            "source_id": "canvas_assignments",
            "source_name": "Canvas Assignments",
            "data": [{'assignments': canvas_grades[section_label]["canvas_assignments"]}]
        })

        

        section_data["assignments"].append({
            "source_id": "canvas_quizzes",
            "source_name": "Canvas Quizzes",
            "data": [{'assignments':canvas_grades[section_label]["canvas_quizzes"]}]
        })
            
