"""
This module encapsulates the access of the term data
(including registered summer terms, registered future terms).
"""

import logging
from django.utils import timezone
from datetime import timedelta
from uw_sws.section import (
    get_section_by_label, is_a_term, is_b_term, is_full_summer_term)
from myuw.models import SeenRegistration
from myuw.util.thread import ThreadWithResponse
from myuw.dao.enrollment import enrollment_history
from myuw.dao.term import (
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
    resp_data = {"terms": [],
                 "next_term_data": None}
    enrollment_list = enrollment_history(request)
    bterm_started = False
    high_light = False
    summer_started = False
    has_a_non_summer_quater = False  # handle mock data
    now = get_comparison_datetime(request)

    # Collect enrollments in future terms
    future_term_enrollments = []
    for enrollment in reversed(enrollment_list):
        if enrollment.term.is_past(now):
            break

        if enrollment.term.is_current(now):
            if enrollment.term.is_summer_quarter():
                bterm_started = (now >= enrollment.term.get_eod_summer_aterm())
                if not bterm_started:
                    future_term_enrollments.append(enrollment)
                summer_started = (now >= enrollment.term.get_bod_first_day())
            break

        future_term_enrollments.append(enrollment)

    if len(future_term_enrollments):
        for enrollment in reversed(future_term_enrollments):
            if enrollment.term.is_summer_quarter():
                summer_term_data = _get_summer_term_data(enrollment)
                if not summer_started:
                    data = None
                    if summer_term_data[A_TERM]:
                        data = _get_resp_json(
                            enrollment, "a-term", summer_term_data)
                    else:
                        if (summer_term_data[FULL_TERM] and
                                not summer_term_data[B_TERM]):
                            data = _get_resp_json(
                                enrollment, "full-term", summer_term_data)
                    if data is not None:
                        data["highlight"] = _should_highlight(request, data)
                        high_light = high_light or data["highlight"]
                        resp_data["terms"].append(data)

                if not bterm_started:
                    if summer_term_data[B_TERM] or summer_term_data[FULL_TERM]:
                        data = _get_resp_json(
                            enrollment, "b-term", summer_term_data)
                        bterm_start_dt = timezone.make_aware(
                            enrollment.term.get_eod_summer_aterm())
                        data["highlight"] = (
                            _should_highlight(request, data, bterm_start_dt))
                        high_light = high_light or data["highlight"]
                        resp_data["terms"].append(data)
            else:
                if has_a_non_summer_quater:
                    break
                data = _get_resp_json(enrollment)
                data["highlight"] = _should_highlight(request, data)
                high_light = high_light or data["highlight"]
                resp_data["terms"].append(data)
                resp_data["next_term_data"] = data
                has_a_non_summer_quater = True

        resp_data["highlight_future_quarters"] = high_light
    return resp_data


def _get_resp_json(enrollment, summer_term=None, summer_term_data=None):
    return_json = enrollment.term.json_data()
    return_json["quarter"] = return_json["quarter"].title()
    return_json["summer_term"] = summer_term
    return_json["url"] = "/{},{}".format(enrollment.term.year,
                                         enrollment.term.quarter)
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
        total_sections, total_credits = _get_sections_credits(enrollment)
        return_json["credits"] = str(total_credits)
        return_json["section_count"] = total_sections

    return_json["has_registration"] = return_json["section_count"] > 0
    return return_json


def _get_summer_term_data(enrollment):
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
    # Need the summer_term in the section data
    _get_sections(enrollment.registrations)

    for reg in enrollment.registrations:
        if is_full_summer_term(reg.section.summer_term):
            data[FULL_TERM] = True
            data[FULL_TERM_SECTIONS] += 1
            data[FULL_TERM_CREDITS] = float(reg.credits)
            continue
        if is_a_term(reg.section.summer_term):
            data[A_TERM] = True
            data[A_TERM_SECTIONS] += 1
            data[A_TERM_CREDITS] = float(reg.credits)
            continue
        if is_b_term(reg.section.summer_term):
            data[B_TERM] = True
            data[B_TERM_SECTIONS] += 1
            data[B_TERM_CREDITS] += float(reg.credits)
    return data


def _get_sections(registrations):
    name_threads = {}
    section_registration_dict = {}  # section_label: registration
    for reg in registrations:
        label = reg.section_ref.section_label()
        section_registration_dict[label] = reg
        thread = ThreadWithResponse(target=get_section_by_label, args=(label,))
        name_threads[label] = thread
        thread.start()

    for section_label in name_threads:
        thread = name_threads[section_label]
        thread.join()
        if thread.response:
            section_registration_dict[section_label].section = thread.response


def _get_sections_credits(enrollment):
    total_sections = 0
    total_credits = 0
    for reg in enrollment.registrations:
        total_sections += 1
        total_credits += float(reg.credits)
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
