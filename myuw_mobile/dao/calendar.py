from myuw_mobile.dao.term import get_comparison_date
from myuw_mobile.dao.calendar_mapping import get_calendars_for_current_user
from restclients.trumba import get_calendar_by_name
from datetime import timedelta
import re

# Number of future days to search for displaying events
DISPLAY_CUTOFF_DAYS = 14
# Number of future days to search for displaying link to cal and card
ACTIVE_CUTOFF_DAYS = 30


def api_request(request):
    current_date = get_comparison_date(request)
    calendar_ids = get_calendars_for_current_user(request)
    return get_events(calendar_ids, current_date)


def get_events(dept_cals, now):
    return_data = {'future_active_cals': {},
                   'events': [],
                   'active_cals': {}}
    events_by_cal = {}
    for key in dept_cals:
        cal_id = key
        cal_url = dept_cals[key]
        events_by_cal[cal_id] = {'cal': cal_url,
                                 'events': []}
        t_cal = get_calendar_by_name(cal_id)
        cal_events = []
        for event in t_cal.walk('vevent'):
            cal_events.append(event)

        cal_events = sort_events(cal_events)

        for event in cal_events:
            start = _get_date(event.get('dtstart').dt)
            if start > now:
                if start < now + timedelta(days=14):
                    return_data['events'].append(json_for_event(event,
                                                                cal_url,
                                                                cal_id))
                    title = t_cal.get('x-wr-calname').to_ical()
                    url = get_calendar_url(cal_id)
                    return_data['active_cals'][cal_id] = {'title': title,
                                                          'url': url}
                elif start < now + timedelta(days=30):
                    if cal_id in return_data['future_active_cals']:
                        return_data['future_active_cals'][cal_id]['count'] += 1
                    else:
                        title = t_cal.get('x-wr-calname').to_ical()

                        if cal_url is None:
                            cal_url = get_calendar_url(cal_id)
                        active_data = {'count': 1,
                                       'title': title,
                                       'base_url': cal_url}

                        return_data['future_active_cals'][cal_id] = active_data
    return return_data


def sort_events(events):
    return sorted(events,
                  key=lambda e: _get_date(e.get('dtstart').dt)
                  )


def parse_dates(event):
    start = format_datetime(event.get('dtstart'))
    end = format_datetime(event.get('dtstart'))
    return start, end


def format_datetime(dt):
    return format_native_datetime(dt.dt)


def format_native_datetime(dt):
    return str(dt)


def _get_date(date):
    try:
        return date.date()
    except AttributeError:
        return date
    return date


def parse_event_url(event, cal_url, cal_id):
    uid = event.get('uid')

    matches = re.match('.*?(\d+)$', uid)
    if not matches:
        return

    event_id = matches.group(1)
    base_url = get_calendar_url(cal_id)
    if cal_url is not None:
        base_url = cal_url

    url = base_url \
        + "?trumbaEmbed=view%%3Devent%%26eventid%%3D"\
        + event_id

    return url


def get_calendar_url(calendar_id):
    url = "http://www.trumba.com/calendar/%s" % calendar_id

    return url


def parse_event_location(event):
    return event.get('location')


def json_for_event(event, cal_url, cal_id):
    start, end = parse_dates(event)
    event_url = parse_event_url(event, cal_url, cal_id)
    event_location = parse_event_location(event)

    return {
        "summary": event.get('summary').to_ical(),
        "start": start,
        "end": end,
        "event_url": event_url,
        "event_location": event_location.to_ical(),
    }
