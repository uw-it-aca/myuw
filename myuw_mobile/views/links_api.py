from django.http import HttpResponse
from django.conf import settings
from django.utils import simplejson as json
import logging
from rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.links import Link
from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.util import log_data_not_found_response, log_success_response

class QuickLinks(RESTDispatch):
    """
    Performs actions on resource at /api/v1/links/.
    """
    
    def GET(self, request):
        """
        GET returns 200 with textbooks for the current quarter
        """
        timer = Timer()
        logger = logging.getLogger('myuw_mobile.views.links_api.QuickLinks.GET')
        user = UserService().get_user_model()
        links = Link().get_links_for_user(user)
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
        logger = logging.getLogger('myuw_mobile.views.links_api.QuickLinks.PUT')

        links = json.loads(request.read())
        link_lookup = {}
        for link in links:
            link_lookup[link["id"]] = link["is_on"]

        user = UserService().get_user_model()
        Link().save_link_preferences_for_user(link_lookup, user)
        log_success_response(logger, timer)
        return HttpResponse("")

