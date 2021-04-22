# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import os
from restclients_core.exceptions import DataFailureException
from uw_sws.term import get_current_term
from myuw.dao.gws import is_grad_student
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.enrollment import enrollment_history
from myuw.dao.term import get_comparison_datetime


DEGREE_TYPE_COLUMN_MAP = {"major": 2,
                          "minor": 3,
                          "gradmajor": 4}
CALENDAR_ID_COL = 5
CALENDAR_URL_COL = 6


def get_calendars_for_current_user(request):
    return _get_calendars(request, _get_major_minors(request))


def _get_major_minors(request):
    """
    Collect majors and minors of current and future quarter enrollments
    for current students.
    Return those of their last quarter's for former students.
    """
    majors = []
    minors = []
    result = {'majors': majors, 'minors': minors}
    enrollment_list = enrollment_history(request)
    now = get_comparison_datetime(request)

    for enrollment in reversed(enrollment_list):
        if enrollment.term.is_past(now):
            if len(majors) == 0:
                # no current or future enrollment
                _collect(majors, minors, enrollment)
            return result
        elif enrollment.term.is_current(now):
            _collect(majors, minors, enrollment)
            if len(majors) or len(minors):
                return result
        else:
            _collect(majors, minors, enrollment)
    return result


def _collect(majors, minors, enrollment):
    """
    Collect unique major names and minor short names
    """
    for major in enrollment.majors:
        majr = major.major_name
        if majr and majr not in majors:
            majors.append(majr)

    for minor in enrollment.minors:
        minr = minor.short_name
        if minr and minr not in minors:
            minors.append(minr)


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
    with open(path, 'r', encoding='utf8') as csvfile:
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
