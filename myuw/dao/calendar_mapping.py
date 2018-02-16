import csv
import os
from restclients_core.exceptions import DataFailureException
from uw_sws.term import get_current_term
from myuw.dao.gws import is_grad_student
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.student import get_minors, get_majors


DEGREE_TYPE_COLUMN_MAP = {"major": 2,
                          "minor": 3,
                          "gradmajor": 4}
CALENDAR_ID_COL = 5
CALENDAR_URL_COL = 6


def get_calendars_for_current_user(request):

    try:

        majors = get_majors(request)['rollup']
        majors = [major.major_name for major in majors]

        minors = get_minors(request)['rollup']
        minors = [minor.short_name for minor in minors]

    except DataFailureException:
        majors = []
        minors = []

    enrollments = {
        'majors': majors,
        'minors': minors
    }

    return _get_calendars(request, enrollments)


def _get_calendars(request, enrollments):

    calendars = {}

    calendars.update(get_calendars_for_minors(enrollments['minors']))

    if is_grad_student(request):
        calendars.update(get_calendars_for_gradmajors(enrollments['majors']))
    else:
        calendars.update(get_calendars_for_majors(enrollments['majors']))
    return calendars


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
