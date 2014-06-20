from django.http import HttpResponse
import json
import logging
from myuw_mobile.dao.category_links import get_links_for_category
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found


class CategoryLinks(RESTDispatch):
    """
    Performs actions on resource at /api/v1/categorylinks/.
    """

    def GET(self, request, category):
        """
        GET returns 200 with links for the given category
        """
        timer = Timer()
        logger = logging.getLogger('views.api.CategoryLinks.GET')
        links = get_links_for_category(category)
        if not links:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        link_data = []
        for link in links:
            link_data.append(link.json_data())

        log_success_response(logger, timer)
        return HttpResponse(json.dumps(link_data))

