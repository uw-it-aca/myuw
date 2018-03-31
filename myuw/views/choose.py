import logging
import traceback
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.user import set_preference_to_old_myuw,\
    set_preference_to_new_myuw
from myuw.logger.logresp import log_msg_with_affiliation
from myuw.logger.timer import Timer
from myuw.views import prefetch_resources
from myuw.views.page import redirect_to_legacy_site


logger = logging.getLogger(__name__)


@login_required
def new_site(request):
    timer = Timer()
    set_preference_to_new_myuw(request)
    prefetch_resources(request,
                       prefetch_group=True,
                       prefetch_enrollment=True)
    affi = get_all_affiliations(request)
    log_msg_with_affiliation(logger, timer, affi,
                             add_referer(request, "Choose new myuw"))
    return HttpResponseRedirect(reverse("myuw_home"))


@login_required
def old_site(request):
    timer = Timer()
    set_preference_to_old_myuw(request)
    prefetch_resources(request,
                       prefetch_group=True,
                       prefetch_enrollment=True)
    affi = get_all_affiliations(request)
    log_msg_with_affiliation(logger, timer, affi,
                             add_referer(request, "Choose old myuw"))
    return redirect_to_legacy_site()


def add_referer(request, msg):
    return "%s (Referer: %s)" % (msg, request.META.get('HTTP_REFERER'))
