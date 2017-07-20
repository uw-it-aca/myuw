import logging
import traceback
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from myuw.dao.user import set_preference_to_new_myuw,\
    set_preference_to_old_myuw, get_netid_of_current_user
from myuw.logger.logresp import log_msg_with_affiliation
from myuw.logger.timer import Timer
from myuw.views.page import redirect_to_legacy_site


logger = logging.getLogger(__name__)


@login_required
def new_site(request):
    timer = Timer()
    set_preference_to_new_myuw(get_netid_of_current_user())
    log_msg_with_affiliation(logger, timer, request, "Choose new myuw")
    return HttpResponseRedirect(reverse("myuw_home"))


@login_required
def old_site(request):
    timer = Timer()
    set_preference_to_old_myuw(get_netid_of_current_user())
    log_msg_with_affiliation(logger, timer, request, "Choose old myuw")
    return redirect_to_legacy_site()
