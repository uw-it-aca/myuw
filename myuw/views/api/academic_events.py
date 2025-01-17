# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta, datetime
import icalendar
import re
import json
import logging
import traceback
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.dao.instructor import is_instructor
from myuw.dao.term import get_comparison_date, get_current_quarter
from uw_trumba import get_calendar_by_name
from uw_sws.term import get_term_after

CURRENT_LIST_MAX_DAYS = 3
logger = logging.getLogger(__name__)
QUARTERS = ['Winter', 'Spring', 'Summer', 'Autumn']


def get_term_before(quarter, year):
    prev_year = year
    prev_quarter = QUARTERS[QUARTERS.index(quarter) - 1]
    if prev_quarter == "Autumn":
        prev_year -= 1
    return prev_quarter, prev_year


class AcademicEvents(ProtectedAPI):
    """
    Performs actions on /api/v1/academic_events
    """
    def get(self, request, *args, **kwargs):
        current = kwargs.get('current', False)
        timer = Timer()
        try:
            events = []

            cal_names = ['sea_acad-inst', 'sea_acad-holidays']
            if is_instructor(request):
                cal_names = cal_names + ['sea_acad-regi', 'sea_acad-grade']

            calendars = []
            for cal in cal_names:
                calendars.append(get_calendar_by_name(cal))

            raw_events = []
            index = 0
            for calendar in calendars:
                for event in calendar.walk('vevent'):
                    event.add("calendar_name", cal_names[index])
                    raw_events.append(event)
                index = index + 1

            raw_events = self.sort_events(raw_events)

            raw_events = self.categorize_events(raw_events)

            raw_events = self.filter_past_events(request, raw_events)

            if current:
                raw_events = self.filter_non_current(request, raw_events)
            else:
                raw_events = self.filter_too_future_events(request, raw_events)

            for event in raw_events:
                events.append(self.json_for_event(event))
            log_api_call(timer, request, "Get AcademicEvents")
            return self.json_response(events)
        except Exception:
            return handle_exception(logger, timer, traceback)

    def json_for_event(self, event):
        year, quarter = self.parse_year_quarter(event)
        start, end = self.parse_dates(event)
        json_data = {
            "summary": event.get('summary'),
            "start": start,
            "end": end,
            "year": int(year),
            "quarter": quarter,
            "category": self.parse_category(event),
            "myuw_categories": self.parse_myuw_categories(event),
            "event_url": self.parse_event_url(event),
            "is_all_day": self.parse_event_is_all_day(event),
        }
        if (json_data['myuw_categories']['term_breaks'] and
                year and quarter):
            pquarter, pyear = get_term_before(quarter, int(year))
            json_data['quarter'] = pquarter
            json_data['year'] = pyear
            # so it is displayed before the quarter

        return json_data

    def _get_year_qtr_from_cur_term(self, event, request):
        current = get_current_quarter(request)
        start = self.get_start_date(event)
        if current.first_day_quarter <= start <= current.last_final_exam_date:
            return current.year, current.quarter.capitalize()
        return None, None

    def parse_myuw_categories(self, event):
        return json.loads(event.get('myuw_categories'))

    def parse_event_is_all_day(self, event):
        start = event.get('dtstart')
        end = event.get('dtend')

        diff = end.dt - start.dt
        if diff.days == 1 and diff.seconds == 0:
            return True

        return False

    def parse_category(self, event):
        value = event.get("categories")
        return (
            value.to_ical().decode()
            if value and isinstance(value, icalendar.prop.vCategory)
            else value)

    def parse_event_url(self, event):
        uid = event.get('uid')

        matches = re.match(r'.*?(\d+)$', uid)
        if not matches:
            return

        event_id = matches.group(1)

        url = ("http://www.washington.edu/calendar/academic/"
               "?trumbaEmbed=view%3Devent%26eventid%3D{}".format(event_id))

        return url

    def parse_dates(self, event):
        return (self.format_datetime(event.get('dtstart')),
                self.format_native_datetime(self.event_end_date(event)))

    def event_end_date(self, event):
        return self.get_end_date(event) - timedelta(days=1)

    def parse_year_quarter(self, event):
        year = None
        quarter = None
        # MUWM-5230
        custom_fields = event.get('X-TRUMBA-CUSTOMFIELD')
        if custom_fields:
            for value in custom_fields:
                if value in QUARTERS:
                    quarter = value
                    break
            for value in custom_fields:
                if value.isnumeric():
                    year = value
                    break
        if None in (year, quarter):
            logger.error(
                "Missing year/quarter in acad-cal event: {}".format(event))
        return year, quarter

    def format_datetime(self, dt):
        return self.format_native_datetime(dt.dt)

    def format_native_datetime(self, dt):
        return str(dt)

    def categorize_events(self, events):
        for event in events:
            categories = json.dumps(self.get_event_categories(event))
            event.add("myuw_categories", categories)
        return events

    def get_event_categories(self, event):
        categories = {
            'breaks': False,
            'classes': False,
            'grade': False,
            'registration': False,
            'term_breaks': False
        }

        cate_value = self.parse_category(event)
        if cate_value:
            if "Grade" in cate_value:
                categories["grade"] = True

            if "Registration" in cate_value:
                categories["registration"] = True

            if "Holidays" in cate_value:
                categories["breaks"] = True

            if "Instruction" in cate_value:
                categories["classes"] = True

                summary = event.get('summary')
                if re.match(r'.* Break.*', summary, flags=re.IGNORECASE):
                    categories["breaks"] = True
                    categories["term_breaks"] = True

        return categories

    def get_start_date(self, event):
        start = event.get('dtstart').dt
        if isinstance(start, datetime):
            start = start.date()
        return start

    def get_end_date(self, event):
        end = event.get('dtend').dt
        if isinstance(end, datetime):
            end = end.date()
        return end

    def sort_events(self, events):
        return sorted(events,
                      key=lambda e: self.get_start_date(e)
                      )

    def filter_past_events(self, request, events):
        comparison_date = get_comparison_date(request)

        non_past = []
        for event in events:
            # Events' end dates are midnight of the next day - not what we want
            # muwm-2489
            end_date = self.event_end_date(event)
            if end_date >= comparison_date:
                non_past.append(event)

        return non_past

    def filter_too_future_events(self, request, events):
        current = get_current_quarter(request)
        after = get_term_after

        last_date = None
        # MUWM-2522
        # This is intended as a workaround for missing data, but it's proably
        # also good enough if there's an error fetching a term resource
        # against live resources.
        try:
            last = after(after(after(after(current))))
            last_date = last.grade_submission_deadline.date()
        except Exception as ex:
            last_dt = (current.grade_submission_deadline + timedelta(days=365))
            last_date = last_dt.date()

        not_too_future = []
        for event in events:
            start = self.get_start_date(event)
            if start <= last_date:
                not_too_future.append(event)

        return not_too_future

    def filter_non_current(self, request, events):
        comparison_date = get_comparison_date(request)
        last_date = comparison_date + timedelta(days=7*4)

        ok_overlaps = {}
        round1 = []
        for event in events:
            if self.get_start_date(event) <= last_date:
                # The comparison date is the first date of the event in
                # the ideal event window (now -> 4 weeks from now)
                start = self.get_start_date(event)
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
                start = self.get_start_date(event)
                date_string = self.format_native_datetime(start)
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
