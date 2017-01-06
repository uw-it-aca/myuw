"""
This class encapsulates the interactions with
the uwnetid subscription resource.
"""

import logging
from datetime import date, datetime, timedelta
from restclients.uwnetid.password import get_uwnetid_password
from restclients.exceptions import DataFailureException
from myuw.dao.term import get_comparison_datetime_with_tz


logger = logging.getLogger(__name__)


def get_password_info(uwnetid):
    """
    returns restclients.models.uwnetid.UwPassword object
    for a given uwnetid
    """
    if uwnetid is None:
        return None
    return get_uwnetid_password(uwnetid)


def get_pw_json(uwnetid, request):
    """
    return data attributes:
    {
    "uwnetid":
    "netid_status": list of strings
    "has_active_med_pw": boolean
    "last_change_med": date
    "days_after_last_med_pw_change": interger
    "expires_med": date
    "interval_med": seconds
    "med_pw_expired": boolean
    "last_change": date
    "days_after_last_pw_change": integer
    "interval": seconds or null
    "minimum_length": integer
    "time_stamp": date
    "kerb_status": string
    }
    """
    pw = get_password_info(uwnetid)
    now_dt = get_comparison_datetime_with_tz(request)

    json_data = pw.json_data()
    json_data["days_after_last_pw_change"] =\
        get_days_after(pw.last_change, now_dt)
    json_data["has_active_med_pw"] = False

    if pw.last_change_med:
        json_data["has_active_med_pw"] = True

        json_data["days_after_last_med_pw_change"] =\
            get_days_after(pw.last_change_med, now_dt)

        if pw.expires_med < now_dt:
            json_data["med_pw_expired"] = True
        else:
            json_data["med_pw_expired"] = False
            json_data["days_before_med_pw_expires"] =\
                get_days_before(pw.expires_med, now_dt)

            if json_data["days_before_med_pw_expires"] <= 30:
                json_data["expires_in_30_days_or_less"] = True
            else:
                json_data["expires_in_30_days_or_less"] = False

    return json_data


def get_days_after(last_change_dt, now_dt):
    delta = now_dt - last_change_dt
    return delta.days


def get_days_before(expires_dt, now_dt):
    delta = expires_dt - now_dt
    return delta.days
