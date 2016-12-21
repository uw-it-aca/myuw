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
    pw = get_password_info(uwnetid)
    now_dt = get_comparison_datetime_with_tz(request)

    json_data = pw.json_data()

    if pw.is_kerb_status_disabled():
        json_data["kerb_status_disabled"] = True
    else:
        json_data["kerb_status_disabled"] = False

    if pw.is_kerb_status_expired():
        json_data["kerb_status_expired"] = True
    else:
        json_data["kerb_status_expired"] = False

    json_data["days_after_last_pw_change"] =\
        get_days_after_last_change(pw.last_change, now_dt)

    if pw.is_kerb_status_active() and pw.last_change_med:

        json_data["has_active_med_pw"] = True

        json_data["days_after_last_med_pw_change"] =\
            get_days_after_last_change(pw.last_change_med, now_dt)

        json_data["days_before_med_pw_expires"] =\
            get_days_before_expires(pw.expires_med, now_dt)

        if json_data["days_before_med_pw_expires"] <= 30:
            json_data["expires_in_30_days_or_less"] = True
        else:
            json_data["expires_in_30_days_or_less"] = False

    return json_data


def get_days_after_last_change(last_change_dt, now_dt):
    delta = now_dt - last_change_dt
    return delta.days


def get_days_before_expires(expires_dt, now_dt):
    delta = expires_dt - now_dt
    return delta.days
