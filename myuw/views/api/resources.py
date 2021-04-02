# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.dao import is_action_disabled
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception
from myuw.dao.category_links import (
    Resource_Links, pin_category, delete_categor_pin)
from myuw.views.exceptions import DisabledAction

logger = logging.getLogger(__name__)


class ResourcesList(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/resources/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the student account balances
        of the current user
        """
        timer = Timer()
        try:
            links = Resource_Links()
            grouped = links.get_all_grouped_links(request)
            log_api_call(timer, request, "Get ResourcesList")
            return self.json_response(grouped)
        except Exception:
            return handle_exception(logger, timer, traceback)


class ResourcesPin(ProtectedAPI):
    """
    Pins and unpins explore cards at /api/v1/resources/<cat+subcat>/pin
    """

    def post(self, request, *args, **kwargs):
        """
        POST returns a 200 creating the pin record
        """
        timer = Timer()
        category_id = kwargs['category_id'].lower()
        try:
            if is_action_disabled():
                raise DisabledAction("Overriding can't Pin category {}".format(
                    category_id))

            pin_category(request, category_id)
            log_api_call(timer, request,
                         "Pin category {}".format(category_id))
        except Exception:
            return handle_exception(logger, timer, traceback)
        return self.html_response("")

    def delete(self, request, *args, **kwargs):
        """
        DELETE returns a 200 deleting the pin record
        """
        timer = Timer()
        category_id = kwargs['category_id'].lower()
        try:
            if is_action_disabled():
                raise DisabledAction(
                    "Overriding can't Unpin category {}".format(category_id))

            delete_categor_pin(request, category_id)
            log_api_call(timer, request,
                         "Unpin category {}".format(category_id))
        except Exception:
            return handle_exception(logger, timer, traceback)
        return self.html_response("")


class PinnedResources(ProtectedAPI):
    """
    Returns of all pinned resources for the given user
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns a 200 with the user's pinned resources
        """
        timer = Timer()
        try:
            links = Resource_Links()
            grouped = links.get_pinned_links(request)
            log_api_call(timer, request, "Get PinnedResources")
            return self.json_response(grouped)
        except Exception:
            return handle_exception(logger, timer, traceback)
