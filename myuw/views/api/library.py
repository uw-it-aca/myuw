# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from myuw.dao.library import get_account_info_for_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class MyLibInfo(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/library/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the library account balances
        of the current user
        """
        timer = Timer()
        try:
            myaccount = get_account_info_for_current_user(request)
            resp_json = myaccount.json_data()
            log_api_call(timer, request, "Get My Library Account")
            return self.json_response(resp_json)
        except Exception:
            return handle_exception(logger, timer, traceback)
