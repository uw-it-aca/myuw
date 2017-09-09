from dateutil.relativedelta import *

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
    start_date = None
    end_date = None
    sections = []



