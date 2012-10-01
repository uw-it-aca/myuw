from django.http import HttpResponse
from django.conf import settings
from django.utils import simplejson as json
import logging
from rest_dispatch import RESTDispatch
from myuw_mobile.dao.links import Link
from myuw_mobile.user import UserService
from myuw_mobile.dao.pws import Person as PersonDao
from myuw_mobile.user import UserService

class QuickLinks(RESTDispatch):
    """
    Performs actions on resource at /api/v1/links/.
    """
    _logger = logging.getLogger('myuw_mobile.views.links_api.QuickLinks')

    def GET(self, request):
        """
        GET returns 200 with textbooks for the current quarter
        """
        
        user_service = UserService(request)
        links = Link(user_service).get_links_for_user()
        link_data = []

        for link in links:
            link_data.append(link.json_data())

        return HttpResponse(json.dumps(link_data))


    def PUT(self, request):
        """
        PUT saves whether links are turned on or off.
        """

        user_service = UserService(request)
        links = json.loads(request.read())
        link_lookup = {}
        for link in links:
            link_lookup[link["id"]] = link["is_on"]

        Link(user_service).save_link_preferences_for_user(link_lookup)
        return HttpResponse("")

