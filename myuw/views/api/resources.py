import logging
import traceback
from myuw.logger.timer import Timer
from myuw.logger.logresp import (
    log_data_not_found_response, log_msg, log_success_response)
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, handle_exception
from myuw.dao.category_links import (
    Resource_Links, pin_category, delete_categor_pin)
from myuw.exceptions import InvalidResourceCategory
from myuw.models import ResourceCategoryPin

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
            grouped = links.get_grouped_links()
            log_success_response(logger, timer)
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
            pin_category(request, category_id)
        except InvalidResourceCategory as ex:
            return handle_exception(logger, timer, traceback)

        return self.html_response("")

    def delete(self, request, *args, **kwargs):
        """
        DELETE returns a 200 deleting the pin record
        """
        timer = Timer()
        category_id = kwargs['category_id'].lower()
        try:
            delete_categor_pin(request, category_id)
        except ResourceCategoryPin.DoesNotExist as ex:
            return handle_exception(logger, timer, traceback)

        return self.html_response("")