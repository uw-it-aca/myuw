import csv
import os
from myuw.dao.gws import is_grad_student
from myuw.dao.student_profile import get_cur_future_enrollments


DEGREE_TYPE_COLUMN_MAP = {"major": 2,
                          "minor": 3,
                          "gradmajor": 4}
CALENDAR_ID_COL = 5
CALENDAR_URL_COL = 6


def get_calendars_for_current_user(request):
    return _get_calendars(request, _get_enrollments(request))


def _get_calendars(request, enrollments):
    calendars = {}
    calendars.update(get_calendars_for_minors(enrollments['minors']))
    if is_grad_student(request):
        calendars.update(get_calendars_for_gradmajors(enrollments['majors']))
    else:
        calendars.update(get_calendars_for_majors(enrollments['majors']))
    return calendars


def _get_enrollments(request):
    majors = []
    minors = []
    try:
        terms, enrollments = get_cur_future_enrollments(request)
        for enrollment in enrollments.values():
            if len(enrollment.majors) > 0:
                for major in enrollment.majors:
                    if major.major_name and major.major_name not in majors:
                        majors.append(major.major_name)

            if len(enrollment.minors) > 0:
                for minor in enrollment.minors:
                    if minor.short_name and minor.short_name not in minors:
                        minors.append(minor.short_name)
    except Exception:
        pass
    return {'majors': majors,
            'minors': minors}


def get_calendars_for_majors(majors):
    return _get_calendars_by_name_and_type(majors, 'major')


def get_calendars_for_minors(minors):
    return _get_calendars_by_name_and_type(minors, 'minor')


def get_calendars_for_gradmajors(gradmajors):
    return _get_calendars_by_name_and_type(gradmajors, 'gradmajor')


def _get_calendars_by_name_and_type(major_name, major_type):
    calendars = {}
    degree_column = DEGREE_TYPE_COLUMN_MAP[major_type]

    path = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'calendar_major_mapping.csv')
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            degree_name = row[degree_column].strip()
            if degree_name in major_name and \
                    len(row[CALENDAR_ID_COL]) > 0:
                base_url = None
                if len(row[CALENDAR_URL_COL]) > 0:
                    base_url = row[CALENDAR_URL_COL]
                cal_ids = _get_calendar_ids_from_text(row[CALENDAR_ID_COL])
                for cal_id in cal_ids:
                    calendars[cal_id] = base_url
    return calendars


def _get_calendar_ids_from_text(text):
    return text.split(" ")
