"""
The Member class encapsulates the interactions
with the UW Netid Web Service
"""

import logging
from restclients_core.exceptions import DataFailureException
from uw_uwnetid.models import Subscription
from uw_uwnetid.subscription import get_netid_subscriptions
from uw_uwnetid.subscription_60 import select_kerberos,\
    has_clinician_in_permits
from uw_uwnetid.subscription_64 import select_2fa
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def is_clinician():
    """
    Return True if the current user netid is
    a member of the UW Med Center Workforce
    """
    try:
        subs = select_kerberos(get_subscriptions())
        if subs:
            return has_clinician_in_permits(subs.permits)
        return False
    except DataFailureException as ex:
        if ex.status == 404:
            return False
        else:
            raise


def is_2fa_permitted():
    """
    Return True if the current user netid is 2fa permitted
    """
    try:
        status = select_2fa(get_subscriptions())
        return status and status.permitted
    except DataFailureException as ex:
        if ex.status == 404:
            return False
        else:
            raise


def get_subscriptions():
    return get_netid_subscriptions(
        get_netid_of_current_user(),
        [Subscription.SUBS_CODE_KERBEROS, Subscription.SUBS_CODE_2FA])


def uwnetid_prefetch():
    def _method(request):
        return get_subscriptions()
    return [_method]
