import csv
import os
from myuw.dao.term import get_comparison_date, get_current_quarter


"""
Gets the thrive message for the current day/quarter
"""


def get_current_message(request):
    current_date = get_comparison_date(request)
    current_qtr = get_current_quarter(request)
    messages = _get_message_for_quarter_date(current_date, current_qtr)
    return messages


def _get_message_for_quarter_date(current_date, term):
    offset = _get_offset(current_date, term)

    path = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'thrive_content.csv')
    with open(path, 'rbU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # skip headers
        next(reader)
        for row in reader:
            try:
                if len(row[3]) > 0:
                    if _is_displayed(row, term.quarter, offset):
                        return _make_thrive_payload(row)
            except IndexError:
                pass


"""
Return true if message is for current quarter and current date falls within the
display range for a given message.  Message will display for 7 days.
"""


def _is_displayed(row, current_quarter, current_offset):
    display_quarter = row[2]
    display_offset = int(row[3])

    return current_quarter == display_quarter and \
        (display_offset + 7) > current_offset >= display_offset


"""
Builds a message payload from a given thrive message row
"""


def _make_thrive_payload(row):
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
               'urls': _make_urls(row)}

    return payload


"""
Supports up to 5 URLS per row as defined in the spec
"""


def _make_urls(row):
    urls = []
    for i in range(9, 17, 2):
        try:
            if len(row[i]) > 0 and len(row[i+1]) > 0:
                urls.append({'title': row[i],
                             'href': row[i + 1]})
        except IndexError:
            return urls

    return urls



"""
Calculates the offset from the current date and start of quarter date
"""


def _get_offset(current_date, term):
    start_date = term.first_day_quarter
    return (current_date - start_date).days
