from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.term import get_comparison_date, get_current_quarter
from restclients.trumba import get_calendar_by_name
from restclients.sws.term import get_term_after
from django.http import HttpResponse
from datetime import timedelta
import json
import re

CURRENT_LIST_MAX_DAYS = 3


class AcademicEvents(RESTDispatch):
    """
    Performs actions on /api/v1/academic_events
    """
    def GET(self, request, current=False):
        events = []

        cal_names = ['sea_acad-comm', 'sea_acad-inst', 'sea_acad-holidays']

        calendars = []
        for cal in cal_names:
            calendars.append(get_calendar_by_name(cal))

        raw_events = []
        for calendar in calendars:
            for event in calendar.walk('vevent'):
                raw_events.append(event)

        raw_events = self.sort_events(raw_events)

        raw_events = self.filter_past_events(request, raw_events)

        if current:
            raw_events = self.filter_non_current(request, raw_events)
        else:
            raw_events = self.filter_too_future_events(request, raw_events)

        for event in raw_events:
            events.append(self.json_for_event(event))

        return HttpResponse(json.dumps(events))

    def json_for_event(self, event):
        year, quarter = self.parse_year_quarter(event)
        start, end = self.parse_dates(event)
        category = self.parse_category(event)
        event_url = self.parse_event_url(event)

        is_all_day = self.parse_event_is_all_day(event)

        return {
            "summary": event.get('summary'),
            "start": start,
            "end": end,
            "year": year,
            "quarter": quarter,
            "category": category,
            "event_url": event_url,
            "is_all_day": is_all_day,
        }

    def parse_event_is_all_day(self, event):
        start = event.get('dtstart')
        end = event.get('dtend')

        diff = end.dt - start.dt
        if diff.days == 1 and diff.seconds == 0:
            return True

        return False

    def parse_category(self, event):
        return event.get('categories')

    def parse_event_url(self, event):
        uid = event.get('uid')

        matches = re.match('.*?(\d+)$', uid)
        if not matches:
            return

        event_id = matches.group(1)

        url = ("http://www.washington.edu/calendar/academic/"
               "?trumbaEmbed=view%%3Devent%%26eventid%%3D%s" % (event_id))

        return url

    def parse_dates(self, event):
        return (self.format_datetime(event.get('dtstart')),
                self.format_datetime(event.get('dtend')))

    def parse_year_quarter(self, event):
        desc = event.get('description')

        if not desc:
            return None, None

        matches = re.match(".*Year: (\d{4})\s+Quarter: (\w+).*", desc)
        if matches:
            return matches.group(1), matches.group(2)

        else:
            matches = re.match(".*Year: (\d{4}).*", desc)
            if matches:
                return matches.group(1), None

        return None, None

    def format_datetime(self, dt):
        return self.format_native_datetime(dt.dt)

    def format_native_datetime(self, dt):
        return str(dt)

    def sort_events(self, events):
        return sorted(events,
                      key=lambda e: e.get('dtstart').dt
                      )

    def filter_past_events(self, request, events):
        comparison_date = get_comparison_date(request)

        non_past = []
        for event in events:
            if event.get('dtend').dt >= comparison_date:
                non_past.append(event)

        return non_past

    def filter_too_future_events(self, request, events):
        current = get_current_quarter(request)
        after = get_term_after
        last = after(after(after(after(current))))

        not_too_future = []
        for event in events:
            start = event.get('dtstart').dt
            if start <= last.grade_submission_deadline.date():
                not_too_future.append(event)

        return not_too_future

    def filter_non_current(self, request, events):
        comparison_date = get_comparison_date(request)
        last_date = comparison_date + timedelta(days=7*4)

        ok_overlaps = {}
        round1 = []
        for event in events:
            if event.get('dtstart').dt <= last_date:
                # The comparison date is the first date of the event in
                # the ideal event window (now -> 4 weeks from now)
                start = event.get('dtstart').dt
                if start < comparison_date:
                    start = comparison_date

                date_string = self.format_native_datetime(start)
                # We only want to show events from the first 3 days that
                # overlap though
                if date_string not in ok_overlaps:
                    if len(ok_overlaps.keys()) >= CURRENT_LIST_MAX_DAYS:
                        # We've hit our 4th day -
                        # return the values we've collected
                        return round1
                    else:
                        # Track the new date
                        ok_overlaps[date_string] = True

                # This event is in that first 3 matching days
                round1.append(event)
            else:
                start = event.get('dtstart')
                date_string = self.format_datetime(start)
                # There's an event outside of 4 weeks.  3 things can happen:
                # 1) we already have events, and the event's start date isn't
                #    in the ok_overlaps lookup
                #    - return what we have, we're outside the window
                # 2) we don't have any events
                #    - this is the first event, and it's outside the ideal
                #      window.  we want to show all events from this day
                # 3) we have events, and today's date is in ok_overlaps.
                #    - this is not the first event of the day, but it is a day
                #      of events we want to include.
                if len(round1) == 0:
                    # Case 2
                    ok_overlaps[date_string] = True
                if date_string in ok_overlaps:
                    # Case 3, or a continuation of case 2
                    round1.append(event)
                else:
                    # Case 1
                    return round1

        # If all of our events were in the first 3 days...
        return round1
