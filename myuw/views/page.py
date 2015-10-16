import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
from django.conf import settings
import logging
from userservice.user import UserService
from myuw.dao.term import get_current_quarter
from myuw.dao.pws import is_student
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.affiliation import is_mandatory_switch_user
from myuw.dao.affiliation import is_optin_switch_user, has_legacy_preference
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_data_not_found_response
from myuw.logger.logresp import log_invalid_netid_response
from myuw.logger.logresp import log_success_response_with_affiliation
from myuw.views.rest_dispatch import invalid_session
from myuw.dao.uwemail import get_email_forwarding_for_current_user
from myuw.dao.card_display_dates import get_card_visibilty_date_values
from myuw.logger.session_log import log_session

LOGOUT_URL = "/user_logout"


@login_required
def index(request,
          year=None,
          quarter=None,
          summer_term=None):

    netid = UserService().get_user()
    if not netid:
        log_invalid_netid_response(logger, timer)
        return invalid_session()

    if _is_mobile(request):
        # On mobile devices, all students get the current myuw.  Non-students
        # are sent to the legacy site.
        if not is_student():
            return redirect_to_legacy_site()
    else:
        # On the desktop, we're migrating users over.  There are 2 classes of
        # users - mandatory and opt-in switchers.  The mandatory users, who
        # are users who haven't been at the UW long enough to be accustomed to
        # the existing myuw.
        # The other class of users can opt to use the legacy myuw instead.
        # Check to see if they have a set preference, and if not, keep them on
        # the new version
        if not is_mandatory_switch_user():
            if is_optin_switch_user():
                if has_legacy_preference():
                    return redirect_to_legacy_site()
            else:
                return redirect_to_legacy_site()

    timer = Timer()
    logger = logging.getLogger('myuw.views.page.index')

    context = {
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term,
        "home_url": "/",
        "err": None,
        "user": {
            "netid": None,
            "affiliations": get_all_affiliations(request)
        },
        "card_display_dates": get_card_visibilty_date_values(request),
    }

    context["user"]["session_key"] = request.session.session_key
    log_session(netid, request.session.session_key, request)
    my_uwemail_forwarding = get_email_forwarding_for_current_user()
    if my_uwemail_forwarding is not None and my_uwemail_forwarding.is_active():
        c_user = context["user"]
        c_user["email_is_uwgmail"] = my_uwemail_forwarding.is_uwgmail()
        c_user["email_is_uwlive"] = my_uwemail_forwarding.is_uwlive()

    context["user"]["netid"] = netid
    if year is None or quarter is None:
        cur_term = get_current_quarter(request)
        if cur_term is None:
            context["err"] = "No current quarter data!"
            log_data_not_found_response(logger, timer)
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter
    else:
        pass
    log_success_response_with_affiliation(logger, timer, request)
    return render_to_response("index.html",
                              context,
                              context_instance=RequestContext(request))


def _is_mobile(request):
    user_agent = request.META.get("HTTP_USER_AGENT")

    # This is the check we were doing in our apache config...
    if re.match('.*iPhone.*', user_agent):
        return True

    if re.match('.*Android.*Mobile.*', user_agent):
        return True
    return False


def redirect_to_legacy_site():
    legacy_url = getattr(settings,
                         "MYUW_USER_SERVLET_URL",
                         "https://myuw.washington.edu/servlet/user")
    return HttpResponseRedirect(legacy_url)


def logout(request):
    # Expires current myuw session
    django_logout(request)
    logout_url = "%s%s" % ("https://weblogin.washington.edu/",
                           "?logout_action=1&two=myuw&one=myuw.washington.edu")

    # Redirects to weblogin logout page
    return HttpResponseRedirect(logout_url)
