from django.http import HttpResponse
from myuw.logger.logresp import log_client_side_action
from django.contrib.auth.decorators import login_required


@login_required
def log_interaction(request, interaction_type):
    log_client_side_action(request, interaction_type)
    return HttpResponse()
