from myuw.dao.schedule import get_current_quarter_schedule
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.dao.course_color import get_colors_by_schedule
from myuw.dao.term import get_current_quarter
from restclients_core.exceptions import DataFailureException
from dateutil.relativedelta import *
from datetime import timedelta
import math
import copy


def get_schedule_json(visual_schedule, term):
    response = {}
    schedule_periods = []
    period_id = 0
    for period in visual_schedule:
        period_data = period.json_data()
        if period.is_finals:
            period_data['id'] = 'finals'
        else:
            period_data['id'] = period_id
        schedule_periods.append(period_data)
        period_id += 1

    response['periods'] = schedule_periods

    # Add term data for schedule
    response['term'] = {
        'year': term.year,
        'quarter': term.quarter,
        'last_final_exam_date': term.last_final_exam_date
    }
    return response


def get_future_visual_schedule(term):
    schedule = _get_combined_future_schedule(term)
    return _get_visual_schedule_from_schedule(schedule)


def get_current_visual_schedule(request):
    schedule = _get_combined_schedule(request)
    return _get_visual_schedule_from_schedule(schedule)


def _get_combined_schedule(request):
    current_term = get_current_quarter(request)
    try:
        student_schedule = get_current_quarter_schedule(request)
        _set_student_sections(student_schedule)
    except DataFailureException:
        student_schedule = None

    try:
        instructor_schedule = get_instructor_schedule_by_term(current_term)
        _set_instructor_sections(instructor_schedule)
    except DataFailureException:
        instructor_schedule = None

    schedule = None
    if student_schedule is not None:
        schedule = student_schedule
        if instructor_schedule is not None:
            schedule.sections += instructor_schedule.sections
    elif instructor_schedule is not None:
        schedule = instructor_schedule

    return schedule


def _get_combined_future_schedule(term):
    try:
        student_schedule = get_schedule_by_term(term)
        _set_student_sections(student_schedule)
    except DataFailureException:
        student_schedule = None

    try:
        instructor_schedule = get_instructor_schedule_by_term(term)
        _set_instructor_sections(instructor_schedule)
    except DataFailureException:
        instructor_schedule = None

    schedule = None
    if student_schedule is not None:
        schedule = student_schedule
        if instructor_schedule is not None:
            schedule.sections += instructor_schedule.sections
    elif instructor_schedule is not None:
        schedule = instructor_schedule

    return schedule


def _set_instructor_sections(instructor_schedule):
    for section in instructor_schedule.sections:
        section.is_teaching = True
    return instructor_schedule


def _set_student_sections(student_schedule):
    for section in student_schedule.sections:
        section.is_teaching = False
    return student_schedule


def _get_visual_schedule_from_schedule(schedule):
    _add_course_colors_to_schedule(schedule)
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
        weeks = trim_section_meetings(weeks)
        weeks = trim_weeks_no_meetings(weeks)
        consolidated = _consolidate_weeks(weeks)

    _add_weekend_meeting_data(consolidated)
    finals = _get_finals_period(schedule)
    if len(finals.sections) > 0:
        consolidated.append(finals)
    return consolidated


def _add_course_colors_to_schedule(schedule):
    colors = get_colors_by_schedule(schedule)
    for section in schedule.sections:
        try:
            color = colors[section.section_label()]
            section.color_id = color
        except KeyError:
            pass
    return schedule


def _get_finals_period(schedule):
    finals = SchedulePeriod()
    finals.is_finals = True
    finals.sections = copy.deepcopy(schedule.sections)
    return finals


def trim_weeks_no_meetings(weeks):
    trimmed_weeks = copy.copy(weeks)
    for week in weeks:
        non_meeting_sections = []
        for section in week.sections:
            for meeting in section.meetings:
                if meeting.no_meeting() and not meeting.wont_meet():
                    non_meeting_sections.append(section)
        if len(non_meeting_sections) == len(week.sections):
            trimmed_weeks.remove(week)
    return trimmed_weeks


def trim_section_meetings(weeks):
    for week in weeks:
        for section in week.sections:
            if section.start_date > week.start_date:
                trimmed = _trim_section_before(section, section.start_date)
                if trimmed:
                    week.meetings_trimmed = True
            if section.end_date < week.end_date:
                trimmed = _trim_section_after(section, section.end_date)
                if trimmed:
                    week.meetings_trimmed = True
    return weeks


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


def _trim_section_after(section, date):
    cutoff_day = int(date.strftime('%w'))
    trimmed = False
    for meeting in section.meetings:
        if cutoff_day <= 5:
            if meeting.meets_saturday:
                trimmed = True
            meeting.meets_saturday = False
        if cutoff_day <= 4:
            if meeting.meets_friday:
                trimmed = True
            meeting.meets_friday = False
        if cutoff_day <= 3:
            if meeting.meets_thursday:
                trimmed = True
            meeting.meets_thursday = False
        if cutoff_day <= 2:
            if meeting.meets_wednesday:
                trimmed = True
            meeting.meets_wednesday = False
        if cutoff_day <= 1:
            if meeting.meets_tuesday:
                trimmed = True
            meeting.meets_tuesday = False
        if cutoff_day <= 0:
            if meeting.meets_monday:
                trimmed = True
            meeting.meets_monday = False
    return trimmed


def _trim_section_before(section, date):
    cutoff_day = int(date.strftime('%w'))
    trimmed = False
    for meeting in section.meetings:
        if cutoff_day >= 1:
            if meeting.meets_sunday:
                trimmed = True
            meeting.meets_sunday = False
        if cutoff_day >= 2:
            if meeting.meets_monday:
                trimmed = True
            meeting.meets_monday = False
        if cutoff_day >= 3:
            if meeting.meets_tuesday:
                trimmed = True
            meeting.meets_tuesday = False
        if cutoff_day >= 4:
            if meeting.meets_wednesday:
                trimmed = True
            meeting.meets_wednesday = False
        if cutoff_day >= 5:
            if meeting.meets_thursday:
                trimmed = True
            meeting.meets_thursday = False
        if cutoff_day >= 6:
            if meeting.meets_friday:
                trimmed = True
            meeting.meets_friday = False
    return trimmed


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
                # make a copy of section as we'll modify meetings per week
                week.sections.append(copy.deepcopy(section))
    return weeks


def _consolidate_weeks(weeks):
    consolidated_weeks = []
    prev_week = None

    for week in weeks:
        if prev_week is None:
            prev_week = week
        else:
            will_merge = True
            # Don't merge last week of A-term
            if week.summer_term == "A-term" \
                    and weeks.index(week) == len(weeks) - 1:
                will_merge = False
            # Don't merge 2nd week of B term with 1st
            elif week.summer_term == "B-term" and weeks.index(week) == 1:
                will_merge = False
            else:
                #  Merge weeks with same sections
                if _section_lists_are_same(prev_week.sections, week.sections):
                    will_merge = True
                else:
                    will_merge = False
            if week.meetings_trimmed or prev_week.meetings_trimmed:
                will_merge = False

            if will_merge:
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
        self.is_finals = False

        # sections will be either A term OR B term, full term classes will
        # be split into corresponding A and B term pieces
        self.summer_term = None
        self.meetings_trimmed = False

    def json_data(self):
        section_data = []
        for section in self.sections:
            section_json = section.json_data()
            section_json['color_id'] = section.color_id
            section_json['is_teaching'] = section.is_teaching
            section_data.append(section_json)
        data = {'start_date': self.start_date,
                'end_date': self.end_date,
                'meets_saturday': self.meets_saturday,
                'meets_sunday': self.meets_sunday,
                'sections': section_data}
        return data
