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

        calendars = [get_calendar_by_name('sea_acad-cal'),]

        for calendar in calendars:
            for event in calendar.walk('vevent'):
                events.append(self.json_for_event(event))

        return HttpResponse(json.dumps(events))


    def json_for_event(self, event):
        year, quarter = self.parse_year_quarter(event)
        start, end = self.parse_dates(event)
        category = self.parse_category(event)

        return {
            "summary": event.get('summary'),
            "start": start,
            "end": end,
            "year": year,
            "quarter": quarter,
            "category": category,
        }

    def parse_category(self, event):
        return event.get('categories')

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
