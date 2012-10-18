from django.http import HttpResponse
import logging
from myuw_mobile.dao.links import Link
from myuw_mobile.logger.logback import log_info
from myuw_mobile.views.rest_dispatch import data_not_found

def log_interaction(request, interaction_type):
    logger = logging.getLogger('myuw_mobile.views.logger')

    if interaction_type != None:
        log_info(logger,
                    "Interaction: %s" % interaction_type)

    return HttpResponse()

