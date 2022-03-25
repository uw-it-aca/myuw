# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import traceback
import logging
from myuw.dao.persistent_messages import BannerMessage
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class PersistentMsg(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET returns 200, myuw_persistent_messages
        """
        timer = Timer()
        try:
            data = BannerMessage(request).get_message_json()
            log_api_call(timer, request, "Get PersistentMsg")
            return self.json_response(data)
        except Exception:
            return handle_exception(logger, timer, traceback)
