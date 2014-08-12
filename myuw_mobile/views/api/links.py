from django.http import HttpResponse
from django.conf import settings
import json
import logging
from myuw_mobile.dao.links import get_links_for_user, save_link_preferences_for_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found


class QuickLinks(RESTDispatch):
    """
    Performs actions on resource at /api/v1/links/.
    """

    def GET(self, request):
        """
        GET returns 200 with textbooks for the current quarter
        """
        timer = Timer()
        logger = logging.getLogger('views.api.links.QuickLinks.GET')
        links = get_links_for_user()
        if not links:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        link_data = []
        for link in links:
            link_data.append(link.json_data())

        log_success_response(logger, timer)
        return HttpResponse(json.dumps(link_data))


    def PUT(self, request):
        """
        PUT saves whether links are turned on or off.
        """
        timer = Timer()
        logger = logging.getLogger('views.api.links.QuickLinks.PUT')

        links = json.loads(request.read())
        link_lookup = {}
        for link in links:
            link_lookup[link["id"]] = link["is_on"]

        save_link_preferences_for_user(link_lookup)
        log_success_response(logger, timer)
        return HttpResponse("")


