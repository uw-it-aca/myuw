# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import time
import traceback
from myuw.dao.attestation import get_covid19_vaccination
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class Covid19Attestation(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/covid19/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the covid19_vaccination data
        of the current user
        """
        timer = Timer()
        try:
            covid19_vaccination = get_covid19_vaccination(request)
            log_api_call(timer, request, "Get covid19_vaccination")
            return self.json_response(covid19_vaccination.json_data())
        except Exception as ex:
            return handle_exception(logger, timer, traceback)
