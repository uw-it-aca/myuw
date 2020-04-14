"""
The Member class encapsulates the interactions
with the UW Netid Web Service
"""

import logging
import traceback
from uw_uwnetid.models import Subscription
from uw_uwnetid.subscription import get_netid_subscriptions
from uw_uwnetid.subscription_105 import get_uwemail_forwarding
from myuw.dao import get_netid_of_current_user, log_err

logger = logging.getLogger(__name__)
kerberos_id = Subscription.SUBS_CODE_KERBEROS
uforwarding_id = Subscription.SUBS_CODE_U_FORWARDING
twofa_id = Subscription.SUBS_CODE_2FA


def is_2fa_permitted(request):
    """
    return True if has 2fa permitted
    """
    return get_subscriptions(request).get(twofa_id)


def get_email_forwarding_for_current_user(request):
    """
    returns UwEmailForwarding object for the current user
    """
    return get_subscriptions(request).get(uforwarding_id)


def get_subscriptions(request):
    if hasattr(request, "myuwnetid_subscriptions"):
        return request.myuwnetid_subscriptions

    subs_dict = {uforwarding_id: None,
                 kerberos_id: None,
                 twofa_id: False}
    netid = get_netid_of_current_user(request)
    try:
        subscriptions = get_netid_subscriptions(
            netid, [kerberos_id, twofa_id, uforwarding_id])

        for subs in subscriptions:
            if (subs.subscription_code == uforwarding_id):
                subs_dict[uforwarding_id] = get_uwemail_forwarding(subs)
                # a UwEmailForwarding object

            if (subs.subscription_code == kerberos_id):
                subs_dict[kerberos_id] = subs.permits
                # a list of SubscriptionPermit objects

            if (subs.subscription_code == twofa_id):
                subs_dict[twofa_id] = subs.permitted
                # True|False

    except Exception:
        log_err(logger, "uwnetid_subscriptions({})".format(netid),
                traceback, request)

    request.myuwnetid_subscriptions = subs_dict
    return subs_dict


def subscriptions_prefetch():
    def _method(request):
        get_subscriptions(request)
    return [_method]
