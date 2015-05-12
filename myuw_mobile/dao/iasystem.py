from datetime import datetime
from restclients.pws import PWS
from restclients.exceptions import DataFailureException
from restclients.iasystem import evaluation
from myuw_mobile.dao.student_profile import get_profile_of_current_user
from myuw_mobile.dao.term import get_comparison_date, term_matched


def get_evaluations_by_section(section):
    profile = get_profile_of_current_user()
    return _get_evaluations_by_section_and_student(section,
                                                   profile.student_number)


def _get_evaluations_by_section_and_student(section, student_id):
    try:
        search_params = {'year': section.term.year,
                         'term_name': section.term.quarter.capitalize(),
                         'curriculum_abbreviation': section.curriculum_abbr,
                         'course_number': section.course_number,
                         'section_id': section.section_id,
                         'student_id': student_id}
        return evaluation.search_evaluations(section.course_campus.lower(),
                                             **search_params)

    except DataFailureException:
        return None


def json_for_evaluation(request, evaluations, section_summer_term):
    now = get_comparison_date(request)
    # this_morning = datetime(now.year, now.month, now.day, 0, 0, 0)
    json_data = {'instructors': [],
                 'open_date': None,
                 'close_date': None}
    for evaluation in evaluations:
        if evaluation.eval_is_online and \
                term_matched(request, section_summer_term):
            # this_morning < evaluation.eval_close_date
            eval_json = {}

            pws = PWS()
            instructor = \
                pws.get_person_by_employee_id(evaluation.instructor_id)

            eval_json['instructor_name'] = instructor.display_name
            eval_json['instructor_title'] = instructor.title1
            json_data['close_date'] = evaluation.eval_close_date.isoformat()
            json_data['open_date'] = evaluation.eval_open_date.isoformat()
            eval_json['url'] = evaluation.eval_url
            json_data['instructors'].append(eval_json)

    return json_data

# def get_evaluations_for_student_term(term):
#     profile = get_profile_of_current_user()
#     return _get_evaluation_by_student_number(profile.student_number, term)
#
#
# def _get_evaluation_by_student_number(student_number, term):
#     seattle = None
#     bothell = None
#     tacoma = None
#     try:
#         seattle = evaluation.search_evaluations("seattle",
#                                                 year=term.year,
#                                                 term_name=term.quarter.capitalize(),
#                                                 student_id=student_number)
#     except DataFailureException:
#         pass
#     try:
#         tacoma = evaluation.search_evaluations("tacoma",
#                                                year=term.year,
#                                                term_name=term.quarter.capitalize(),
#                                                student_id=student_number)
#     except DataFailureException:
#         pass
#     try:
#         bothell = evaluation.search_evaluations("bothell",
#                                                 year=term.year,
#                                                 term_name=term.quarter.capitalize(),
#                                                 student_id=student_number)
#     except DataFailureException:
#         pass
#
#     return {'seattle': seattle,
#             'bothell': bothell,
#             'tacoma': tacoma}
