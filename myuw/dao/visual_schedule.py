from dateutil.relativedelta import *
from datetime import timedelta


def get_visual_schedule(schedule):

    _add_dates_to_sections(schedule)
    bounds = get_schedule_bounds(schedule)
    periods = get_periods_from_bounds(bounds)


def get_periods_from_bounds(bounds):
    start, end = bounds
    periods = []

    current_date = start
    while(current_date > end):
        period = SchedulePeriod()
        # period.start_date =
        current_date = current_date + relativedelta(weeks=1)

        # while start_week <= end_week:

        # period = SchedulePeriod()
        # period.create_from_week_num_year(start_week, start.strftime('%Y'))
        #
        # periods[start_week] = period
        # start_week += 1


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
    schedule_length = ((end-start).days + 1)/7

    while schedule_length > 0:
        period = SchedulePeriod()
        period.start_date = start
        period.end_date = (start + timedelta(days=6))
        periods.append(period)
        start = (start + timedelta(days=7))
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
    if start.strftime('%w') != 0:
        days_to_remove = int(start.strftime('%w'))
        start = start - relativedelta(days=days_to_remove)

    # set end to last saturday
    if end.strftime('%w') != 6:
        days_to_add = 6 - int(end.strftime('%w'))
        end = end + relativedelta(days=days_to_add)
    return start, end


def _add_dates_to_sections(schedule):
    """
    Adds term start/end dates to sections that do not have them (ie non-PCE)
    """
    for section in schedule.sections:
        if section.start_date is None:
            # TODO: Handle summer term
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
