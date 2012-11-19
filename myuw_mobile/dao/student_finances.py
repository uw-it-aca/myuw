from django.conf import settings
import logging
import traceback
from myuw_mobile.dao.pws import Person
from myuw_mobile.restclients.hfs_accounts import HfsAccounts
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception, log_info

class Accounts():
    """
    This class encapsulates the interactions with 
    the student account balances (MyUW HFS) web service.
    """
    _logger = logging.getLogger('myuw_mobile.dao.student_finances.Accounts')

    def get_balances(self):
        """
        returns Account Balancess for the current user
        """
        student_number = Person().get_student_number()
        if student_number is None:
            return None

        timer = Timer()
        account_data = None
        try:
            account_data = HfsAccounts().get_balances(student_number)
        except Exception as ex:
            log_exception(Accounts._logger, 
                         'HfsAccounts.get_balances', 
                          traceback.format_exc())
        finally:
            log_resp_time(Accounts._logger,
                         'HfsAccounts.get_balances',
                          timer)

        log_info(Accounts._logger, account_data.json_data())
        return account_data
