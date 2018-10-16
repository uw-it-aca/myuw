from django.http import HttpResponse
from myuw.logger.logresp import log_interaction
from django.contrib.auth.decorators import login_required


@login_required
def log_interaction(request, interaction_type):
    log_interaction(request, interaction_type)
    return HttpResponse()
