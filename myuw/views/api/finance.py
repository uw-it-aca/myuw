import logging
import traceback
from myuw.dao.finance import get_account_balances_for_current_user
from myuw.dao.notice import get_tuition_due_date
from myuw.dao.pws import is_student
from myuw.logger.timer import Timer
from myuw.logger.logresp import (
    log_data_not_found_response, log_msg, log_success_response)
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, handle_exception

logger = logging.getLogger(__name__)


class Finance(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/finance/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the student account balances
        of the current user
        """
        timer = Timer()
        try:
            if not is_student(request):
                log_msg(logger, timer, "Not a student, abort!")
                return data_not_found()

            balances = get_account_balances_for_current_user(request)

            date = get_tuition_due_date(request)
            response = balances.json_data()
            response['tuition_due'] = str(date)

            log_success_response(logger, timer)
            return self.json_response(response)
        except KeyError:
            return handle_exception(logger, timer, traceback)
