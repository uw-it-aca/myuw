import logging
from myuw.logger.timer import Timer
from myuw.dao.thrive import get_current_message, get_previous_messages
from myuw.logger.logresp import (
    log_data_not_found_response, log_success_response)
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found
from myuw.dao.hx_toolkit_dao import get_article_by_id

logger = logging.getLogger(__name__)


class ThriveMessages(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/thrive/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with current thrive message
        for the current user if they are a first year student
        """
        timer = Timer()
        message = None
        if request.GET.get('history', False):
            message = get_previous_messages(request)
        else:
            message = get_current_message(request)

        if message is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        return self.json_response(message)


class HxToolkitMessage(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/hx_toolkit/(article_id).
    """
    def get(self, request,  *args, **kwargs):
        """
        GET returns 200 with current thrive message
        for the current user if they are a first year student
        """
        article_id = kwargs.get('article_id')
        article = get_article_by_id(article_id)
        if article:
            return self.html_response(article)
        else:
            return data_not_found()
