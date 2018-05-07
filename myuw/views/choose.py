import logging
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from myuw.dao.user_pref import set_preference_to_old_myuw,\
    set_preference_to_new_myuw
from myuw.logger.logresp import log_msg_with_request
from myuw.logger.timer import Timer
from myuw.views.page import redirect_to_legacy_site


logger = logging.getLogger(__name__)


@login_required
def new_site(request):
    timer = Timer()
    set_preference_to_new_myuw(request)
    log_msg_with_request(logger, timer, request,
                         add_referer(request, "Chose new myuw"))
    return HttpResponseRedirect(reverse("myuw_home"))


@login_required
def old_site(request):
    timer = Timer()
    set_preference_to_old_myuw(request)
    log_msg_with_request(logger, timer, request,
                         add_referer(request, "Chose old myuw"))
    return redirect_to_legacy_site()


def add_referer(request, msg):
    return "%s (Referer: %s)" % (msg, request.META.get('HTTP_REFERER'))
