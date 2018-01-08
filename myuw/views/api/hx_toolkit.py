import logging
from myuw.logger.timer import Timer
from myuw.dao.thrive import get_current_message, get_previous_messages
from myuw.logger.logresp import (
    log_data_not_found_response, log_success_response)
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found
from myuw.dao.hx_toolkit_dao import get_rendered_article_by_id,\
    get_article_of_week_by_request, get_article_links


class HxToolkitMessage(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/hx_toolkit/(article_id).
    """
    def get(self, request,  *args, **kwargs):
        """
        GET returns 200 with the specified article html
        """
        article_id = kwargs.get('article_id')

        article = get_rendered_article_by_id(article_id)
        if article:
            return self.html_response(article)
        else:
            return data_not_found()


class HxToolkitWeekMessage(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/hx_toolkit/week.
    """
    def get(self, request,  *args, **kwargs):
        """
        GET returns 200 with current weekly article short html
        """

        article = get_article_of_week_by_request(request)
        if article:
            return self.html_response(article)
        else:
            return data_not_found()


class HxToolkitMessageList(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/hx_toolkit/list.
    """
    def get(self, request,  *args, **kwargs):
        """
        GET returns 200 with a list of links to all articles, by category
        """
        summary_data = get_article_links()
        return self.json_response(summary_data)
