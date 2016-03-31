"""
This module provides utility the following functions:
1. categorize notices based on the dictionary defined
   in notice_categorization.py;
2. apply show/hide on notices besed on their category and timing;
3. convert notice object into json format
"""
import logging
from datetime import datetime, timedelta
from myuw.dao.notice_categorization import NOTICE_CATEGORIES
from myuw.dao.term import get_comparison_datetime_with_tz


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
    in myuw.dao.notice_categorization
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
    now = get_comparison_datetime_with_tz(request)
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


def get_est_reg_info(request, notice):
    ret = {"is_today_the_est_reg_date": False,
           "my_reg_has_opened": False}
    now = get_comparison_datetime_with_tz(request)
    for attribute in notice.attributes:
        if attribute.data_type == "date" and\
                attribute.name == "Date":
            ret["is_my_1st_reg_day"] =\
                (now.date() == attribute._date_value.date())

            reg_start = attribute._date_value + timedelta(hours=6)
            ret["my_reg_has_opened"] = (now >= reg_start)
    return ret


def get_json_for_notices(request, notices):
    """
    @return the json data of notices with the specific show/hide logic
    applied on the corresponding notices.
    """
    notice_json = []
    if not notices:
        return notice_json

    for notice in apply_showhide(request, notices):

        if notice.notice_category == "StudentFinAid" and\
                notice.notice_type.endswith("Short") and\
                notice.long_notice is not None:
            data = notice.long_notice.json_data(
                include_abbr_week_month_day_format=True)
            data['short_content'] = notice.notice_content
            data['category'] = notice.custom_category
            data['is_critical'] = False
            data['id_hash'] = notice.id_hash
            data['is_read'] = notice.is_read
            data['location_tags'] = notice.location_tags

        else:
            data = notice.json_data(
                include_abbr_week_month_day_format=True)
            data['category'] = notice.custom_category
            data['sws_category'] = notice.notice_category
            data['is_critical'] = notice.is_critical
            data['id_hash'] = notice.id_hash
            data['is_read'] = notice.is_read
            data['location_tags'] = notice.location_tags

            if "est_reg_date" in notice.location_tags:
                est_reg = get_est_reg_info(request, notice)
                data["is_my_1st_reg_day"] =\
                    est_reg["is_my_1st_reg_day"]
                data["my_reg_has_opened"] =\
                    est_reg["my_reg_has_opened"]

        notice_json.append(data)
    return notice_json
