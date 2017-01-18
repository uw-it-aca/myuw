"""
This class encapsulates the interactions with
the uwnetid subscription resource.
"""

import logging
from restclients.uwnetid.subscription import get_email_forwarding
from restclients.exceptions import DataFailureException
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def _get_email_forwarding_by_uwnetid(uwnetid):
    """
    returns restclients.models.uwnetid.UwEmailForwarding object
    for a given uwnetid
    """
    if uwnetid is None:
        return None
    return get_email_forwarding(uwnetid)


def get_email_forwarding_for_current_user():
    return _get_email_forwarding_by_uwnetid(get_netid_of_current_user())


def email_forwarding_prefetch():
    def _method(request):
        get_email_forwarding_for_current_user()

    return [_method]
