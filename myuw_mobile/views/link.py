from django.http import HttpResponse, HttpResponseRedirect
import logging
from myuw_mobile.dao.links import get_link_by_id
from myuw_mobile.logger.logresp import log_affiliation
from myuw_mobile.views.rest_dispatch import data_not_found

def show_link(request, linkid):
    logger = logging.getLogger('myuw_mobile.views.link')

    link = get_link_by_id(linkid)

    if link == None:
        return data_not_found()

    log_affiliation(logger, 
                    "Opened link id: %s, url: %s" % (linkid, link.url))

    return HttpResponseRedirect(link.url)

