from datetime import datetime
from django.utils import timezone
from restclients.pws import PWS
from restclients.exceptions import DataFailureException
from restclients.iasystem import evaluation
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.term import get_comparison_datetime, is_b_term,\
    convert_to_begin_of_day, get_current_summer_term,\
    get_bod_7d_before_last_instruction, get_eod_current_term


def get_evaluations_by_section(section):
    return _get_evaluations_by_section_and_student(
        section, get_profile_of_current_user().student_number)


def _get_evaluations_by_section_and_student(section, student_number):
    try:
        search_params = {'year': section.term.year,
                         'term_name': section.term.quarter.capitalize(),
                         'curriculum_abbreviation': section.curriculum_abbr,
                         'course_number': section.course_number,
                         'section_id': section.section_id,
                         'student_id': student_number}
        return evaluation.search_evaluations(section.course_campus.lower(),
                                             **search_params)

    except DataFailureException:
        return None


def summer_term_overlaped(request, given_section):
    """
    @return true if:
    1). this is not a summer quarter or
    2). the given_summer_term is overlaped with the
        current summer term in the request
    """
    current_summer_term = get_current_summer_term(request)
    if given_section is None or current_summer_term is None:
        return True
    return (given_section.is_same_summer_term(current_summer_term) or
            given_section.is_full_summer_term() and
            is_b_term(current_summer_term))


def json_for_evaluation(request, evaluations, section):
    if evaluations is None:
        return None
    local_tz = timezone.get_current_timezone()
    now = local_tz.localize(get_comparison_datetime(request))

    # the start date of the default show window
    show_date = get_bod_7d_before_last_instruction(request)
    on_dt = local_tz.localize(convert_to_begin_of_day(show_date))

    # the end date of the default show window
    hide_date = get_eod_current_term(request, True)
    off_dt = local_tz.localize(convert_to_begin_of_day(hide_date))

    if now < on_dt or now > off_dt:
        return None

    pws = PWS()
    json_data = []
    for evaluation in evaluations:
        if summer_term_overlaped(request, section):
            if now < evaluation.eval_open_date or\
                    now >= evaluation.eval_close_date:
                continue

            if evaluation.eval_close_date < off_dt:
                off_dt = evaluation.eval_close_date

            json_item = {'instructors': [],
                         'url': evaluation.eval_url,
                         'is_multi_instr': len(evaluation.instructor_ids) > 1}

            for eid in evaluation.instructor_ids:
                instructor_json = {}
                instructor = pws.get_person_by_employee_id(eid)
                instructor_json['instructor_name'] = instructor.display_name
                instructor_json['instructor_title'] = instructor.title1
                json_item['instructors'].append(instructor_json)

            json_data.append(json_item)
    # althrough each item has its own close date, we
    # only take one - the earliest.
    if len(json_data) > 0:
        return {'evals': json_data,
                'close_date': off_dt.isoformat()}

    return None
