"""
This module provides function to categorize notices based on
the dictionary defined in notice_categorization.py;
function to process notice besed on their category and timing.
"""
import logging
import pytz
from datetime import datetime, timedelta
from django.utils import timezone
from myuw_mobile.dao.notice_categorization import NOTICE_CATEGORIES
from myuw_mobile.dao.term import get_comparison_date


logger = logging.getLogger(__name__)
UNKNOWN_CATEGORY_NAME = "Uncategorized"


def categorize_notices(notices):
    for notice in notices:
        map_notice_category(notice)

    notices[:] = [n for n in notices if n.custom_category != "not a notice"]
    # Removing uncategorized notices for MUWM-2343
    notices[:] = [n for n in notices if
                  n.custom_category != UNKNOWN_CATEGORY_NAME]
    return notices


def map_notice_category(notice):
    """
    Set the custom_category, is_critical, location_tags for
    the given notice based on the NOTICE_CATEGORIES defined
    in myuw_mobile.dao.notice_categorization
    """
    key = notice.notice_category + "_" + notice.notice_type
    categorization = NOTICE_CATEGORIES.get(key, None)
    if categorization is not None:
        notice.custom_category = categorization["myuw_category"]
        notice.is_critical = categorization["critical"]
        notice.location_tags = categorization["location_tags"]
    else:
        notice.custom_category = UNKNOWN_CATEGORY_NAME
        notice.is_critical = False
        notice.location_tags = None
    return notice


def equals_myuwid(notice, value):
    myuw_id = notice.notice_category + "_" + notice.notice_type
    return myuw_id == value


def apply_showhide(request, notices):
    """
    Some financial aid notices have additional show/hide logic
    depending on the open/close dates of the notice.
    This function will apply the show/hide logic on each notice,
    update the notice atttibutes accordingly.
    """
    if notices is None:
        return None
    today = get_comparison_date(request)
    local_tz = timezone.get_current_timezone()
    now = local_tz.localize(
        datetime(today.year,
                 today.month,
                 today.day, 0, 0, 1)).astimezone(pytz.utc)
    for notice in notices:
        if notice.notice_category != "StudentFinAid":
            continue

        if equals_myuwid(notice, "StudentFinAid_AidPriorityDate"):
            # not critical after the first week and
            # before last two weeks
            if is_after_eof_days_after_open(now, notice, 15) and\
                    is_before_bof_days_before_close(now, notice, 15):
                notice.is_critical = False
    return notices


def get_open_date(notice):
    """
    @return the datetime object of the notice begin date value
    in utc timezone
    """
    for attribute in notice.attributes:
        if attribute.data_type == "date" and\
                attribute.name.endswith("Begin"):
            return attribute._date_value


def get_close_date(notice):
    """
    @return the datetime object of the notice end date value
    in utc timezone
    """
    for attribute in notice.attributes:
        if attribute.data_type == "date" and\
                attribute.name.endswith("End"):
            return attribute._date_value


def is_after_eof_days_after_open(now, notice, n_days):
    """
    @return true if it is after "n_days" after the notice open datetime
    """
    return now > get_open_date(notice) + timedelta(days=n_days)


def is_before_bof_days_before_close(now, notice, n_days):
    """
    @return true if it is before "n_days" prior to the notice close datetime
    """
    return now < get_close_date(notice) - timedelta(days=n_days)
