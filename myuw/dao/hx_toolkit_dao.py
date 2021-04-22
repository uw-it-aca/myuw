# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import math
import datetime
from myuw.dao.term import get_current_quarter, get_comparison_date
from hx_toolkit.file_dao import get_rendered_article_by_id, \
    get_article_by_phase_quarter_week, get_article_links_by_category


def get_article_of_week_by_request(request):
    term = get_current_quarter(request)

    phase = _get_phase_by_term(term)

    week = get_week_by_request(request)

    return get_article_by_phase_quarter_week(phase, term.quarter, week)


def get_week_by_request(request):
    term = get_current_quarter(request)
    now = get_comparison_date(request)

    return _get_week_between(term, now)


def _get_week_between(term, now):
    start = term.first_day_quarter
    start = _make_start_sunday(start)
    diff = now - start

    if diff.days > 0:
        diff = diff + datetime.timedelta(1)
        week = int(math.ceil(diff.days/7.0))
    elif diff.days == 0:
        # first week of qtr will be week 1
        week = 1
    else:
        # round down when negative
        week = int(math.floor(diff.days/7.0))
    return week


def _make_start_sunday(date):
    day = date.weekday()
    days_to_subtract = 0
    if day != 6:
        days_to_subtract = day + 1
    date = date - datetime.timedelta(days=days_to_subtract)

    return date


def _get_phase_by_term(term):
    """
    For date override purposes all phases prior to start of will
    default to phase A; a Phase will run from AU of one year through SU of the
    next, ie one 'academic' year
    """
    year = term.year
    quarter = term.quarter

    if quarter == 'autumn':
        year += 1

    phases = ['A', 'B', 'C']
    start_year = 2009
    years_since_start = year - start_year
    phase_offset = 0
    if years_since_start > 0:
        phase_offset = years_since_start % 3
    return phases[phase_offset]


def get_article_links():
    return get_article_links_by_category()
