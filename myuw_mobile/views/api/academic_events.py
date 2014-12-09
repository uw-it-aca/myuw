from myuw_mobile.views.rest_dispatch import RESTDispatch
from restclients.trumba import get_calendar_by_name
from django.http import HttpResponse
import json
import re


class AcademicEvents(RESTDispatch):
    """
    Performs actions on /api/v1/academic_events
    """
    def GET(self, request):
        events = []

        cal_names = ['sea_acad-comm', 'sea_acad-inst', 'sea_acad-holidays']

        calendars = []
        for cal in cal_names:
            calendars.append(get_calendar_by_name(cal))

        for calendar in calendars:
            for event in calendar.walk('vevent'):
                events.append(self.json_for_event(event))

        return HttpResponse(json.dumps(events))

    def json_for_event(self, event):
        year, quarter = self.parse_year_quarter(event)
        start, end = self.parse_dates(event)
        category = self.parse_category(event)
        event_url = self.parse_event_url(event)

        return {
            "summary": event.get('summary'),
            "start": start,
            "end": end,
            "year": year,
            "quarter": quarter,
            "category": category,
            "event_url": event_url,
        }

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
        return str(dt.dt)
