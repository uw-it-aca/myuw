from django.http import HttpResponse
import logging
from myuw.logger.logback import log_info


def log_interaction(request, interaction_type):
    logger = logging.getLogger('myuw.views.logger')

    if interaction_type is not None:
        log_info(logger, "Interaction: %s" % interaction_type)

    return HttpResponse()
