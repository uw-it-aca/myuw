# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from myuw.dao import id_photo_token
from myuw.dao.pws import get_idcard_photo
from myuw.logger.logresp import log_exception
from myuw.views.error import data_not_found

logger = logging.getLogger(__name__)


@login_required
def show_photo(request, uwregid, token):
    if id_photo_token.valid_token(token):
        try:
            photo = get_idcard_photo(uwregid)
            return StreamingHttpResponse(
                [photo.getvalue()], content_type="image/jpeg")
        except Exception:
            log_exception(logger, "get_idcard_photo", traceback)
    return data_not_found()
