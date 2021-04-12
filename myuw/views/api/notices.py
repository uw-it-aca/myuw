# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import traceback
from datetime import datetime
from restclients_core.exceptions import DataFailureException
from myuw.dao import is_action_disabled
from myuw.dao.notice import (
    get_notices_for_current_user, mark_notices_read_for_current_user)
from myuw.dao.notice_mapping import get_json_for_notices
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)
action_logger = logging.getLogger("myuw.views.api.notices.seen")


class Notices(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/notices/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with a list of notices for the current user
                        with an empty array if no notice.
                    543 for data error
        """
        timer = Timer()
        try:
            notice_json = get_json_for_notices(
                request, get_notices_for_current_user(request))

            log_api_call(timer, request, "Get Notices")
            return self.json_response(notice_json)
        except Exception:
            return handle_exception(logger, timer, traceback)

    def put(self, request, *args, **kwargs):
        timer = Timer()
        if not is_action_disabled():
            notice_hashes = json.loads(request.body).get('notice_hashes', None)
            mark_notices_read_for_current_user(request, notice_hashes)
            log_api_call(timer, request,
                         "Put: Read notice {}".format(notice_hashes))
        return self.json_response()
