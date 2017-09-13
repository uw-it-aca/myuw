import csv
import os
import datetime
import logging
from myuw.dao import is_thrive_viewer, get_netid_of_current_user
from myuw.dao.term import get_comparison_date, get_current_quarter,\
    get_bod_current_term_class_start


logger = logging.getLogger(__name__)
TARGET_FYP = "fyp"
TARGET_AUT_TRANSFER = "au_xfer"
TARGET_WIN_TRANSFER = "wi_xfer"
target_groups = [TARGET_AUT_TRANSFER,
                 TARGET_WIN_TRANSFER,
                 TARGET_FYP]
# the order says the priority


def get_target_group():
    uwnetid = get_netid_of_current_user()
    for target in target_groups:
        try:
            if is_thrive_viewer(uwnetid, target):
                return target
        except Exception:
            pass
    return None


def is_fyp():
    return TARGET_FYP == get_target_group()


def is_aut_transfer():
    return TARGET_AUT_TRANSFER == get_target_group()


def is_win_transfer():
    return TARGET_WIN_TRANSFER == get_target_group()


def get_current_message(request):
    """
    Gets the thrive message for the current day in the current quarter
    """
    target = get_target_group()
    if target:
        current_date = get_comparison_date(request)
        current_qtr = get_current_quarter(request)
        messages = _get_messages_for_quarter_dates([current_date],
                                                   current_qtr,
                                                   target)
        if messages and len(messages):
            return messages[0]
    return None


def get_previous_messages(request):
    """
    Gets the thrive messages up to the currrent date in the current quarter
    """
    target = get_target_group()
    if target is None:
        return None

    start_date = get_bod_current_term_class_start(
        request).date() - datetime.timedelta(days=10)
    current_date = get_comparison_date(request)
    current_qtr = get_current_quarter(request)
    messages = []
    dates = []
    if current_date >= start_date:
        while start_date <= current_date:
            dates.append(start_date)
            start_date += datetime.timedelta(days=1)

    messages = _get_messages_for_quarter_dates(dates,
                                               current_qtr,
                                               target)
    return messages


def _get_messages_for_quarter_dates(dates, term, target):
    path = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', "%s_%s" % (target, 'thrive_content.csv'))
    rows = {}
    with open(path, 'rbU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # skip headers
        next(reader)
        for row in reader:
            try:
                if len(row[3]) > 0:
                    for date in dates:
                        offset = _get_offset(date, term)
                        if _is_displayed(row, term.quarter, offset):
                            rows[reader.line_num] = row
                            break
            except IndexError:
                pass

    return ([_make_thrive_payload(rows[row], target)
             for row in sorted(rows.keys())])


def _is_displayed(row, current_quarter, current_offset):
    """
    Return true if message is for current quarter and current date
    falls within the display range for a given message.
    Message will display for 7 days.
    """
    display_quarter = row[2]
    display_offset = int(row[3])

    return current_quarter == display_quarter and \
        (display_offset + 7) > current_offset >= display_offset


def _make_thrive_payload(row, target):
    """
    Builds a message payload from a given thrive message row
    """
    try_this = None
    try:
        if len(row[8]) > 0:
            try_this = row[8]
    except IndexError:
        pass

    payload = {'title': row[6],
               'message': row[7],
               'week_label': row[4],
               'category_label': row[5],
               'try_this': try_this,
               'urls': _make_urls(row),
               'target': target}

    return payload


def _make_urls(row):
    """
    Supports up to 5 URLS per row as defined in the spec
    """
    urls = []
    for i in range(9, 17, 2):
        try:
            if len(row[i]) > 0 and len(row[i+1]) > 0:
                urls.append({'title': row[i],
                             'href': row[i + 1]})
        except IndexError:
            return urls

    return urls


def _get_offset(current_date, term):
    """
    Calculates the offset from the current date and start of quarter date
    """
    start_date = term.first_day_quarter
    return (current_date - start_date).days
