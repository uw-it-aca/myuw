"""
This class encapsulates the interactions with
the SWS Personal Financial resource.
"""
from uw_sws.financial import get_account_balances_by_regid
from myuw.dao.pws import get_regid_of_current_user


def _get_account_balances_by_regid(user_regid):
    """
    returns uw_sws.models.Finance object for a given regid
    """

    if user_regid is None:
        return None

    return get_account_balances_by_regid(user_regid)


def get_account_balances_for_current_user():
    return _get_account_balances_by_regid(get_regid_of_current_user())
