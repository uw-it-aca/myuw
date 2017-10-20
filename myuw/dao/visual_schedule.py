from dateutil.relativedelta import *
from datetime import timedelta
import math


def get_visual_schedule(schedule):
    _add_dates_to_sections(schedule)
    if _is_split_summer(schedule):
        a_bounds, b_bounds = get_summer_schedule_bounds(schedule)
        a_weeks = _get_weeks_from_bounds(a_bounds)

        for week in a_weeks:
            week.summer_term = "A-term"
        a_weeks = _add_sections_to_weeks(schedule.sections, a_weeks)
        a_consolidated = _consolidate_weeks(a_weeks)
        trim_summer_meetings(a_consolidated)

        b_weeks = _get_weeks_from_bounds(b_bounds)
        for week in b_weeks:
            week.summer_term = "B-term"
        b_weeks = _add_sections_to_weeks(schedule.sections, b_weeks)
        b_consolidated = _consolidate_weeks(b_weeks)
        trim_summer_meetings(b_consolidated)

        consolidated = a_consolidated + b_consolidated

    else:
        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        consolidated = _consolidate_weeks(weeks)
    return consolidated


def get_summer_schedule_bounds(schedule):
    a_start = schedule.term.first_day_quarter
    # set start to first sunday
    if a_start.strftime('%w') != 0:
        days_to_remove = int(a_start.strftime('%w'))
        a_start -= relativedelta(days=days_to_remove)

    b_end = schedule.term.last_day_instruction
    # set end to last saturday
    if b_end.strftime('%w') != 6:
        days_to_add = 6 - int(b_end.strftime('%w'))
        b_end += relativedelta(days=days_to_add)

    a_bounds = a_start, schedule.term.aterm_last_date
    b_bounds = schedule.term.bterm_first_date, b_end
    return a_bounds, b_bounds


def trim_summer_meetings(weeks):
    if weeks[0].summer_term == "A-term":
        week_to_trim = weeks[-1]
        week_to_trim.sections = _trim_sections_after(week_to_trim.sections,
                                                     week_to_trim.end_date)
    if weeks[0].summer_term == "B-term":
        week_to_trim = weeks[0]
        week_to_trim.sections = _trim_sections_before(week_to_trim.sections,
                                                      week_to_trim.start_date)

    return weeks


def _trim_sections_after(sections, date):
    cutoff_day = int(date.strftime('%w'))
    for section in sections:
        for meeting in section.meetings:
            if cutoff_day <= 5:
                meeting.meets_saturday = False
            if cutoff_day <= 4:
                meeting.meets_friday = False
            if cutoff_day <= 3:
                meeting.meets_thursday = False
            if cutoff_day <= 2:
                meeting.meets_wednesday = False
            if cutoff_day <= 1:
                meeting.meets_tuesday = False
            if cutoff_day <= 0:
                meeting.meets_monday = False
    return sections


def _trim_sections_before(sections, date):
    cutoff_day = int(date.strftime('%w'))
    for section in sections:
        for meeting in section.meetings:
            if cutoff_day >= 1:
                meeting.meets_sunday = False
            if cutoff_day >= 2:
                meeting.meets_monday = False
            if cutoff_day >= 3:
                meeting.meets_tuesday = False
            if cutoff_day >= 4:
                meeting.meets_wednesday = False
            if cutoff_day >= 5:
                meeting.meets_thursday = False
            if cutoff_day >= 6:
                meeting.meets_friday = False
    return sections


def _is_split_summer(schedule):
    if schedule.term.quarter != 'summer':
        return False
    split = False
    for section in schedule.sections:
        if section.summer_term != "Full-term":
            return True


def _add_weekend_meeting_data(weeks):
    for week in weeks:
        for section in week.sections:
            for meeting in section.meetings:
                if meeting.meets_saturday:
                    week.meets_saturday = True
                if meeting.meets_sunday:
                    week.meets_sunday = True
    return weeks


def _add_sections_to_weeks(sections, weeks):
    for week in weeks:
        for section in sections:
            if section.start_date <= week.end_date \
                    and section.end_date >= week.start_date:
                week.sections.append(section)
    return weeks


def _consolidate_weeks(weeks):
    consolidated_weeks = []
    prev_week = None

    for week in weeks:
        if prev_week is None:
            prev_week = week
        else:
            # Don't merge last week of A-term
            if week.summer_term == "A-term" \
                    and weeks.index(week) == len(weeks) - 1:
                consolidated_weeks.append(prev_week)
                prev_week = week
            # Don't merge 2nd week of B term with 1st
            elif week.summer_term == "B-term" and weeks.index(week) == 1:
                consolidated_weeks.append(prev_week)
                prev_week = week
            else:
                #  Merge weeks with same sections
                if _section_lists_are_same(prev_week.sections, week.sections):
                    prev_week.end_date = week.end_date
                else:
                    consolidated_weeks.append(prev_week)
                    prev_week = week
    # Append last week block
    consolidated_weeks.append(prev_week)
    return consolidated_weeks


def _section_lists_are_same(list1, list2):
    if len(list1) is not len(list2):
        return False

    for l1_section in list1:
        found_match = False
        for l2_section in list2:
            if _sections_are_same(l1_section, l2_section):
                found_match = True
        if not found_match:
            return False
    return True


def _sections_are_same(section1, section2):
    return (section1.curriculum_abbr == section2.curriculum_abbr) \
           and (section1.course_number == section2.course_number) \
           and (section1.section_id == section2.section_id)


def _get_weeks_from_bounds(bounds):
    start, end = bounds
    periods = []

    # weeks between start>end dates, including first day
    schedule_length = math.ceil(((end-start).days + 1)/7.0)

    while schedule_length > 0:
        period = SchedulePeriod()
        period.start_date = start

        start_day = int(start.strftime('%w'))
        end_offset = 6-start_day
        end_date = (start + timedelta(days=end_offset))

        # handle case where week ends midweek
        if end_date > end:
            end_date = end
        period.end_date = end_date

        periods.append(period)

        next_start_offset = 7-start_day
        start = (start + timedelta(days=next_start_offset))
        schedule_length -= 1

    return periods


def get_schedule_bounds(schedule):
    start = None
    end = None
    for section in schedule.sections:
        if start is None:
            start = section.start_date
        elif start > section.start_date:
            start = section.start_date

        if end is None:
            end = section.end_date
        elif end < section.end_date:
            end = section.end_date

    # set start to first sunday
    if int(start.strftime('%w')) != 0:
        days_to_remove = int(start.strftime('%w'))
        start = start - relativedelta(days=days_to_remove)

    # set end to last saturday
    if int(end.strftime('%w')) != 6:
        days_to_add = 6 - int(end.strftime('%w'))
        end += relativedelta(days=days_to_add)
    return start, end


def _add_dates_to_sections(schedule):
    """
    Adds term start/end dates to sections that do not have them (ie non-PCE)
    """
    for section in schedule.sections:
        if section.start_date is None:
            if section.summer_term == "":
                section.start_date = schedule.term.first_day_quarter
                section.end_date = schedule.term.last_day_instruction
            else:
                if section.summer_term == "A-term":
                    section.start_date = schedule.term.first_day_quarter
                    section.end_date = schedule.term.aterm_last_date
                elif section.summer_term == "B-term":
                    section.start_date = schedule.term.bterm_first_date
                    section.end_date = schedule.term.last_day_instruction
                else:
                    section.start_date = schedule.term.first_day_quarter
                    section.end_date = schedule.term.last_day_instruction

    return schedule


class SchedulePeriod():
    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.sections = []
        self.is_boundary_period = False
        self.meets_saturday = False
        self.meets_sunday = False

        # sections will be either A term OR B term, full term classes will
        # be split into corresponding A and B term pieces
        self.summer_term = None
