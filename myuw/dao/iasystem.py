from datetime import datetime
from django.utils import timezone
from restclients.pws import PWS
from restclients.exceptions import DataFailureException
from restclients.iasystem import evaluation
from myuw.dao.student_profile import get_profile_of_current_user
from myuw.dao.term import get_comparison_datetime, is_b_term,\
    get_current_summer_term, get_bod_7d_before_last_instruction,\
    get_eod_current_term


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


def _get_local_tz():
    return timezone.get_current_timezone()


def is_winthin_default_show_windown(request):
    """
    @return true if the comparison date is inside the
    default show window range
    """
    now = _get_local_tz().localize(get_comparison_datetime(request))
    return (now >= _get_default_show_start(request) or
            now < _get_default_show_end(request))


def _get_default_show_start(request):
    """
    @return default show window starting datetime in local time zone
    """
    return _get_local_tz().localize(
        get_bod_7d_before_last_instruction(request))


def _get_default_show_end(request):
    """
    @return default show window ending datetime in local time zone
    """
    return _get_local_tz().localize(get_eod_current_term(request, True))


def json_for_evaluation(request, evaluations, section):
    """
    @return the json format of only the evaluations that
    should be shown.
    The show window starts: 7 days before last inst
    or eveluation openning date, whichever comes later
    The show window ends: the midnight at the end of current term
    grade submission deadline or at the evaluation close date,
    """
    if evaluations is None:
        return None
    now = _get_local_tz().localize(get_comparison_datetime(request))

    on_dt = _get_default_show_start(request)
    off_dt = _get_default_show_end(request)

    if now < on_dt or now >= off_dt:
        return None

    pws = PWS()
    json_data = []
    for evaluation in evaluations:
        if summer_term_overlaped(request, section):
            if evaluation.is_completed or\
                    now < evaluation.eval_open_date or\
                    now >= evaluation.eval_close_date:
                continue

            json_item = {
                'instructors': [],
                'url': evaluation.eval_url,
                'close_date': datetime_str(evaluation.eval_close_date),
                'is_multi_instr': len(evaluation.instructor_ids) > 1}

            for eid in evaluation.instructor_ids:
                instructor_json = {}
                instructor = pws.get_person_by_employee_id(eid)
                instructor_json['instructor_name'] = instructor.display_name
                instructor_json['instructor_title'] = instructor.title1
                json_item['instructors'].append(instructor_json)

            json_data.append(json_item)
    if len(json_data) > 0:
        return {'evals': json_data}

    return None


def datetime_str(localized_datetime):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    return localized_datetime.strftime(fmt)
