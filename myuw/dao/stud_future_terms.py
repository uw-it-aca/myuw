# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module encapsulates the access of the term data
(including registered summer terms, registered future terms).
"""

import logging
from django.utils import timezone
from datetime import timedelta
from restclients_core.exceptions import DataFailureException
from uw_sws.models import Registration
from uw_sws.section import is_a_term, is_b_term, is_full_summer_term
from myuw.models import SeenRegistration
from myuw.dao import is_using_file_dao, get_netid_of_current_user
from myuw.dao.registration import get_schedule_by_term, _is_split_summer
from myuw.dao.term import (
    get_current_quarter, get_next_quarter, get_term_after, get_comparison_date,
    get_comparison_datetime, get_comparison_datetime_with_tz)
from myuw.dao.user import get_user_model

logger = logging.getLogger(__name__)
FULL_TERM = "F"
A_TERM = "A"
B_TERM = "B"

FULL_TERM_CREDITS = "FC"
A_TERM_CREDITS = "AC"
B_TERM_CREDITS = "BC"

FULL_TERM_SECTIONS = "FS"
A_TERM_SECTIONS = "AS"
B_TERM_SECTIONS = "BS"


def get_registered_future_quarters(request):
    """
    Return the list of future quarters that has actively enrolled sections
    """
    resp_data = {"terms": [], "next_term_data": None}
    high_light = False
    future_term_regs, summer_started, bterm_started = (
        _get_future_registrations(request))

    for schedule in future_term_regs:

        if schedule.term.is_summer_quarter():

            summer_term_data = _get_summer_term_data(schedule)
            if _is_split_summer(schedule.registered_summer_terms):

                if (not summer_started and (
                        summer_term_data[A_TERM] or
                        summer_term_data[FULL_TERM])):
                    data = _get_resp_json(schedule, "a-term", summer_term_data)
                    data["highlight"] = _should_highlight(request, data)
                    high_light = high_light or data["highlight"]
                    resp_data["terms"].append(data)

                if (not bterm_started and (
                        summer_term_data[B_TERM] or
                        summer_term_data[FULL_TERM])):
                    data = _get_resp_json(schedule, "b-term", summer_term_data)
                    bterm_start_dt = timezone.make_aware(
                        schedule.term.get_eod_summer_aterm())
                    data["highlight"] = (
                        _should_highlight(request, data, bterm_start_dt))
                    high_light = high_light or data["highlight"]
                    resp_data["terms"].append(data)
                continue

            if not summer_started:
                data = _get_resp_json(schedule, "full-term", summer_term_data)
                data["highlight"] = _should_highlight(request, data)
                high_light = high_light or data["highlight"]
                resp_data["terms"].append(data)
            continue

        # non-summer term
        data = _get_resp_json(schedule)
        data["highlight"] = _should_highlight(request, data)
        high_light = high_light or data["highlight"]
        resp_data["terms"].append(data)
        resp_data["next_term_data"] = data
        resp_data["highlight_future_quarters"] = high_light
    return resp_data


def _get_future_registrations(request):
    data = []
    bterm_started = False
    summer_started = False
    cur_term = get_current_quarter(request)
    nxt_term = get_next_quarter(request)
    if cur_term.is_summer_quarter():
        now = get_comparison_datetime(request)
        summer_started = (now >= cur_term.get_bod_first_day())
        bterm_started = (now >= cur_term.get_eod_summer_aterm())
        if not bterm_started:
            data.append(__get_reg_data(request, cur_term,
                                       summer_term='b-term'))
        data.append(__get_reg_data(request, nxt_term))

    else:
        if nxt_term.is_summer_quarter():
            data.append(__get_reg_data(request, nxt_term))
            data.append(__get_reg_data(request, get_term_after(nxt_term)))
        else:
            data.append(__get_reg_data(request, nxt_term))
    return data, summer_started, bterm_started


def _get_resp_json(schedule, summer_term=None, summer_term_data=None):
    return_json = schedule.term.json_data()
    return_json["quarter"] = return_json["quarter"].title()
    return_json["summer_term"] = summer_term
    return_json["url"] = "/{},{}".format(schedule.term.year,
                                         schedule.term.quarter)
    if summer_term is not None and summer_term_data is not None:
        return_json["url"] = "{},{}".format(return_json["url"], summer_term)

        if summer_term == "a-term":
            return_json["credits"] = str(summer_term_data[FULL_TERM_CREDITS] +
                                         summer_term_data[A_TERM_CREDITS])
            section_count = (summer_term_data[FULL_TERM_SECTIONS] +
                             summer_term_data[A_TERM_SECTIONS])
            return_json["section_count"] = section_count

        elif summer_term == "b-term":
            return_json["credits"] = str(summer_term_data[FULL_TERM_CREDITS] +
                                         summer_term_data[B_TERM_CREDITS])
            section_count = (summer_term_data[FULL_TERM_SECTIONS] +
                             summer_term_data[B_TERM_SECTIONS])
            return_json["section_count"] = section_count

        elif summer_term == "full-term":
            return_json["credits"] = str(summer_term_data[FULL_TERM_CREDITS])
            return_json["section_count"] = summer_term_data[FULL_TERM_SECTIONS]
    else:
        total_sections, total_credits = _get_sections_credits(schedule)
        return_json["credits"] = str(total_credits)
        return_json["section_count"] = total_sections

    return_json["has_registration"] = return_json["section_count"] > 0
    return return_json


def _get_summer_term_data(schedule):
    """
    Return all the summer terms in the registered summer sections
    """
    data = {
        FULL_TERM: False,
        A_TERM: False,
        B_TERM: False,
        FULL_TERM_CREDITS: 0,
        A_TERM_CREDITS: 0,
        B_TERM_CREDITS: 0,
        FULL_TERM_SECTIONS: 0,
        A_TERM_SECTIONS: 0,
        B_TERM_SECTIONS: 0,
        }
    for section in schedule.sections:
        if is_full_summer_term(section.summer_term):
            data[FULL_TERM] = True
            data[FULL_TERM_SECTIONS] += 1
            data[FULL_TERM_CREDITS] += float(section.registration.credits)
            continue
        if is_a_term(section.summer_term):
            data[A_TERM] = True
            data[A_TERM_SECTIONS] += 1
            data[A_TERM_CREDITS] += float(section.registration.credits)
            continue
        if is_b_term(section.summer_term):
            data[B_TERM] = True
            data[B_TERM_SECTIONS] += 1
            data[B_TERM_CREDITS] += float(section.registration.credits)
    return data


def _get_sections_credits(schedule):
    total_sections = 0
    total_credits = 0
    for section in schedule.sections:
        total_sections += 1
        total_credits += float(section.registration.credits)
    return total_sections, total_credits


def _should_highlight(request, data, bterm_start_dt=None):
    # MUWM-2210
    year = data["year"]
    quarter = data["quarter"]
    summer_term = data['summer_term'][0] if data['summer_term'] else ""
    user = get_user_model(request)
    now = get_comparison_datetime_with_tz(request)
    qset = SeenRegistration.objects.filter(user=user,
                                           year=year,
                                           quarter=quarter,
                                           summer_term=summer_term)
    if len(qset) > 1:
        logger.warning(
            "{} with user={}, year={}, quarter={}, summer_term={}".format(
                "Multiple Objects", user.uwnetid, year, quarter, summer_term))
        # MUWM-3137, remove bad data
        qset.delete()

    srobj, is_new = SeenRegistration.objects.get_or_create(
        user=user,
        year=year,
        quarter=quarter,
        summer_term=summer_term,
        defaults={'first_seen_date': now})

    if not is_new:
        if summer_term == 'b':
            # MUWM-3009 highlight in the last week before b-term start
            if now > bterm_start_dt - timedelta(days=8):
                srobj.first_seen_date = now
                srobj.save()

    # highlight on the 1st day when the reg status card shows up
    return now < srobj.first_seen_date + timedelta(days=1)


def __get_reg_data(request, term, summer_term="full-term"):
    if not is_using_file_dao():
        return get_schedule_by_term(
            request, term=term, summer_term=summer_term)

    if get_netid_of_current_user(request) == 'jerror':
        raise DataFailureException("/student/v5/registration.json",
                                   500, "mock 500 error")
    if get_netid_of_current_user(request) == 'none':
        raise DataFailureException("/student/v5/registration.json",
                                   404, "mock 404 error")

    # mock an object with no enrolled sections
    mock_0reg_schedule = Registration()
    mock_0reg_schedule.sections = []
    mock_0reg_schedule.term = term
    mock_0reg_schedule.summer_term = summer_term
    mock_0reg_schedule.registered_summer_terms = {}

    now = get_comparison_date(request)
    if now <= (term.registration_period1_start + timedelta(days=3)):
        # hold reg data until 3 days after registration_period1_start
        return mock_0reg_schedule

    try:
        return get_schedule_by_term(
            request, term=term, summer_term=summer_term)
    except DataFailureException as ex:
        if ex.status == 404:
            # missing mock data
            return mock_0reg_schedule
        raise
