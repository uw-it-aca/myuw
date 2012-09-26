from django.http import HttpResponse
from django.conf import settings
from django.utils import simplejson as json
from rest_dispatch import RESTDispatch
from myuw_mobile.dao.links import Link
from page import get_netid_from_session

class QuickLinks(RESTDispatch):
    """
    Performs actions on resource at /api/v1/links/.
    """
    def GET(self, request):
        """
        GET returns 200 with textbooks for the current quarter
        """
        netid = get_netid_from_session(request);
        if not netid or not PersonDao().get_regid(netid):
            return super(QuickLinks,
                         self).invalid_session(*args, **named_args)
                    
        links = Link().get_links_for_user(netid)
        link_data = []

        for link in links:
            link_data.append(link.json_data())

        return HttpResponse(json.dumps(link_data))



