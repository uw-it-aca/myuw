"""
This class encapsulates the interactions with 
the student account balances (MyUW HFS) web service.
"""

import logging
import traceback
from myuw_mobile.logger.timer import Timer
from myuw_mobile.restclients.hfs_accounts import HfsAccounts
from myuw_mobile.dao.pws import get_student_number, get_employee_id
from restclients.hfs.idcard import get_hfs_accounts
from restclients.models.hfs import StudentHuskyCardAccout, ResidentDiningAccount
from restclients.exceptions import DataFailureException
from myuw_mobile.logger.logback import log_exception, log_resp_time, log_info
from myuw_mobile.dao.pws import get_netid_of_current_user
from restclients.models.hfs import HfsAccouts as AccountsModel


logger = logging.getLogger(__name__)


def get_account_balances_by_uwnetid(uwnetid):
    """
    returns restclients.models.hfs.HfsAccouts
    for the given uwnetid
    """
    if uwnetid is None:
        return None
    id = "%s %s" % ('get_hfs_accounts', uwnetid)

    try:
        return get_hfs_accounts(uwnetid)
    except Exception as ex:
        log_exception(logger, 
                     id,
                      traceback.format_exc())
    return None


def get_legacy_data():
    student_number = get_student_number()
    if student_number is None:
        student_number = "0000000"

    employee_id = get_employee_id()
    if employee_id is None:
        employee_id = "000000000"

    timer = Timer()
    try:
        account_data = HfsAccounts().get_balances(student_number,
                                                  employee_id)

        if account_data is not None:
            log_info(logger, account_data.json_data())
            return account_data
    except Exception as ex:
        log_exception(logger,
                     'HfsAccounts.get_balances',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                     'HfsAccounts.get_balances',
                      timer)
    return None



def get_account_balances_for_current_user():
    # XXX - MUWM-1982
    # Falling back to the old myuw code until we get our network issue sorted out
    #new_values = get_account_balances_by_uwnetid(get_netid_of_current_user())

    old_values = get_legacy_data()

    old_values_obj = AccountsModel()
    print old_values.husky_card, old_values.residence_hall_dining

    if old_values.husky_card:
        old_values_obj.student_husky_card = StudentHuskyCardAccout()
        old_values_obj.student_husky_card.balance = old_values.husky_card
        old_values_obj.student_husky_card.last_updated = old_values.asof_datetime

    if old_values.residence_hall_dining:
        old_values_obj.resident_dining = ResidentDiningAccount()
        old_values_obj.resident_dining.balance = old_values.residence_hall_dining
        old_values_obj.resident_dining.last_updated = old_values.asof_datetime


    return old_values_obj
