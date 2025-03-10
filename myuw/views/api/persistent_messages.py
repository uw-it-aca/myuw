# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import traceback
import logging
from myuw.dao.persistent_messages import BannerMessage as Message
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class BannerMessage(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        """
        GET myuw_banner_message returns 200
        """
        timer = Timer()
        try:
            data = Message(request).get_message_json()
            log_api_call(timer, request, "Get BannerMessage")
            return self.json_response(data)
        except Exception:
            return handle_exception(logger, timer, traceback)
