import csv
import os
from myuw_mobile.dao.enrollment import get_current_quarter_enrollment
from myuw_mobile.dao.gws import is_grad_student


DEGREE_TYPE_COLUMN_MAP = {"major": 2,
                          "minor": 3,
                          "gradmajor": 4}
CALENDAR_ID_COL = 5
CALENDAR_URL_COL = 6


def get_calendars_for_current_user(request):
    return _get_calendars(_get_enrollments(request))


def _get_calendars(enrollments):
    calendars = []
    calendars = calendars + get_calendars_for_minors(enrollments['minors'])
    print (enrollments['minors'])
    print (enrollments['majors'])
    if enrollments['is_grad']:
        grad_cals = get_calendars_for_gradmajors(enrollments['majors'])
        calendars = calendars + grad_cals
    else:
        calendars = calendars + get_calendars_for_majors(enrollments['majors'])

    return calendars


def _get_enrollments(request):
    majors = []
    minors = []

    enrollment = get_current_quarter_enrollment(request)
    if enrollment is not None:
        if len(enrollment.majors) > 0:
            for major in enrollment.majors:
                majors.append(major.degree_abbr)

        if len(enrollment.minors) > 0:
            for minor in enrollment.minors:
                minors.append(minor.abbr)

    return {'is_grad': is_grad_student(),
            'majors': majors,
            'minors': minors}


def get_calendars_for_majors(majors):
    return _get_calendars_by_name_and_type(majors, 'major')


def get_calendars_for_minors(minors):
    return _get_calendars_by_name_and_type(minors, 'minor')


def get_calendars_for_gradmajors(gradmajors):
    return _get_calendars_by_name_and_type(gradmajors, 'gradmajor')


def _get_calendars_by_name_and_type(major_name, major_type):
    calendars = []
    added_calendars = []
    degree_column = DEGREE_TYPE_COLUMN_MAP[major_type]

    path = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'calendar_major_mapping.csv')
    with open(path, 'rbU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if row[degree_column] in major_name and \
                    len(row[CALENDAR_ID_COL]) > 0 and \
                    row[CALENDAR_ID_COL] not in added_calendars:
                base_url = None
                if len(row[CALENDAR_URL_COL]) > 0:
                    base_url = row[CALENDAR_URL_COL]
                cal = {row[CALENDAR_ID_COL]: base_url}
                calendars.append(cal)
                added_calendars.append(row[CALENDAR_ID_COL])
    return calendars
