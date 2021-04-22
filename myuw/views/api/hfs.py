# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import time
import traceback
from myuw.dao.hfs import get_account_balances_for_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class HfsBalances(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/hfs/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the HFS account balances
        of the current user
        """
        timer = Timer()
        try:
            balances = get_account_balances_for_current_user(request)

            resp_json = balances.json_data(use_custom_date_format=True)
            log_api_call(timer, request, "Get Hfs Account Balances")
            return self.json_response(resp_json)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)
