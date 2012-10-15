from django.http import HttpResponse, HttpResponseRedirect
from myuw_mobile.dao.links import Link
from myuw_mobile.logger.logback import log_info
import logging

def show_link(request, linkid):

    link = Link.get_link_by_id(linkid)

    if link == None:
        response = HttpResponse()
        response.status_code = 404
        return response

    logger = logging.getLogger('myuw_mobile.views.link')
    log_info(logger, "Opened link id: %s, url: %s" % (linkid, link.url))

    return HttpResponseRedirect(link.url)

