"""
This class encapsulates the interactions with 
the student account balances (MyUW HFS) web service.
"""

import logging
import traceback
from myuw_mobile.restclients.hfs_accounts import HfsAccounts
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception, log_info
from myuw_mobile.dao.pws import get_student_number, get_employee_id


logger = logging.getLogger(__name__)


def get_account_balances():
    """
    returns HFS Account Balancess for the current user
    """
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
        
