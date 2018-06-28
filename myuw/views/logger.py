from django.http import HttpResponse
import logging
from myuw.logger.logresp import log_msg_with_request
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)

@login_required
def log_interaction(request, interaction_type):
    if interaction_type is not None:
        log_msg_with_request(logger, None, request, interaction_type)
    return HttpResponse()
