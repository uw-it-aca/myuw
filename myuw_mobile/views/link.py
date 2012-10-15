from django.http import HttpResponse, HttpResponseRedirect
import logging
from myuw_mobile.dao.links import Link
from myuw_mobile.logger.logback import log_info
from myuw_mobile.views.rest_dispatch import data_not_found

def show_link(request, linkid):
    logger = logging.getLogger('myuw_mobile.views.link')

    link = Link.get_link_by_id(linkid)

    if link == None:
        return data_not_found()

    log_info(logger, "Opened link id: %s, url: %s" % (linkid, link.url))

    return HttpResponseRedirect(link.url)

