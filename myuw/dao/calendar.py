# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
from datetime import timedelta, datetime, time
from urllib.parse import quote_plus, urlencode
from restclients_core.exceptions import DataFailureException
from uw_trumba import get_calendar_by_name
from myuw.dao.term import (
  DEFAULT_TZ, get_comparison_datetime_with_tz)
from myuw.dao.calendar_mapping import get_calendars_for_current_user


# Number of future days to search for displaying events
DISPLAY_CUTOFF_DAYS = 14
# Number of future days to search for displaying link to cal and card
FUTURE_CUTOFF_DAYS = 30


def api_request(request):
    current_date = get_comparison_datetime_with_tz(request)
    calendar_ids = get_calendars_for_current_user(request)
    return get_events(calendar_ids, current_date)


def get_events(dept_cals, now):
    events = _get_all_events(dept_cals)
    events = _filter_past_events(events, now)
    current_events = _get_current_events(events, now)
    future_events = []
    if len(current_events) == 0:
        future_events = _get_future_events(events, now)

    future_event_json = []
    current_event_json = []
    active_calendar_json = []

    active_cal_ids = []
    current_events = sort_events(current_events)
    for event in current_events:
        json = _get_json_for_event(event)
        current_event_json.append(json)
        if event.cal_id not in active_cal_ids:
            active_cal_json = _get_active_cal_json(event)
            active_calendar_json.append(active_cal_json)
            active_cal_ids.append(event.cal_id)
    if len(future_events) > 0:
        future_event_json = _get_future_event_json(future_events)

    response = {'future_active_cals': future_event_json,
                'active_cals': active_calendar_json,
                'events': current_event_json}
    return response


def _get_future_event_json(events):
    future_cals = {}
    for event in events:
        if event.cal_id not in future_cals:
            url = _get_cal_url_from_event(event)
            future_cals[event.cal_id] = {'base_url': url,
                                         'count': 1,
                                         'title': event.cal_title}
        else:
            future_cals[event.cal_id]['count'] += 1
    future_cal_list = []
    for key in future_cals:
        future_cal_list.append(future_cals[key])
    return future_cal_list


def _get_cal_url_from_event(event):
    url = event.base_url
    if url is None:
        url = get_calendar_url(event.cal_id)
    return url


def _get_active_cal_json(event):
    return {"title": event.cal_title,
            "url": _get_cal_url_from_event(event)}


def _get_json_for_event(event):
    event_location = parse_event_location(event)
    is_allday = _get_is_all_day(event)
    end = event.get('dtend').dt
    if is_allday:
        end = end - timedelta(days=1)

    return {
        "summary": event.get('summary'),
        "start": _get_date(event.get('dtstart').dt).isoformat(),
        "end": _get_date(end).isoformat(),
        "event_url": event.event_url,
        "event_location": event_location,
        "is_all_day": is_allday
    }


def _get_is_all_day(event):
    if event.get('X-MICROSOFT-CDO-ALLDAYEVENT') == "TRUE":
        return True
    else:
        return False


def _get_future_events(events, now):
    max_cutoff = now + timedelta(days=FUTURE_CUTOFF_DAYS)
    min_cutoff = now + timedelta(days=DISPLAY_CUTOFF_DAYS)
    future = []
    for event in events:
        end_date = _get_date(event.get('dtend').dt)
        if min_cutoff <= end_date <= max_cutoff:
            future.append(event)

    return future


def _get_current_events(events, now):
    cutoff = now + timedelta(days=DISPLAY_CUTOFF_DAYS)
    current = []
    for event in events:
        start_date = _get_date(event.get('dtstart').dt)
        if start_date <= cutoff:
            current.append(event)

    return current


def _filter_past_events(events, now):
    non_past = []
    for event in events:
        end_date = _get_date(event.get('dtend').dt)
        if end_date >= now:
            non_past.append(event)
    return non_past


def _get_all_events(dept_cals):
    events = []
    for key in dept_cals:
        cal_id = key
        cal_base_url = dept_cals[key]
        try:
            calendar = get_calendar_by_name(cal_id)
            for event in calendar.walk('vevent'):
                event.event_url = parse_event_url(event, cal_base_url, cal_id)
                event.cal_id = cal_id
                event.base_url = cal_base_url
                event.cal_title = calendar.get(
                    'x-wr-calname').to_ical().decode("utf-8")
                events.append(event)
        except DataFailureException:
            pass
    return events


def sort_events(events):
    return sorted(events, key=lambda e: _get_date(e.get('dtstart').dt))


def parse_event_url(event, cal_url, cal_id):
    uid = event.get('uid')

    matches = re.match(r'.*?(\d+)$', uid)
    if not matches:
        return

    event_id = matches.group(1)
    base_url = get_calendar_url(cal_id)
    if cal_url is not None:
        base_url = cal_url
    url_params = (('eventid', event_id), ('view', 'event'))

    url = "{}?trumbaEmbed={}".format(
        base_url, quote_plus(urlencode(url_params, doseq=True)))

    return url


def get_calendar_url(calendar_id):
    url = "http://www.trumba.com/calendar/{}".format(calendar_id)

    return url


def parse_event_location(event):
    location = event.get('location')
    if location is None:
        location = ""
    return location


def _get_date(date):
    if hasattr(date, 'hour'):
        return date
    datetime_naive = datetime.combine(date, time(hour=0, minute=0))
    return datetime_naive.replace(tzinfo=DEFAULT_TZ)  # MUWM-5318
