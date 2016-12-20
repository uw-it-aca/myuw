import re
import logging
import traceback
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
from django.conf import settings
from django.views.decorators.cache import cache_control
from userservice.user import UserService
from myuw.dao.term import get_current_quarter
from myuw.dao.pws import is_student
from myuw.dao.affiliation import get_all_affiliations, is_oldmyuw_user
from myuw.dao.emaillink import get_service_url_for_address
from myuw.dao.exceptions import EmailServiceUrlException
from myuw.logger.timer import Timer
from myuw.logger.logback import log_exception
from myuw.logger.logresp import log_invalid_netid_response
from myuw.logger.logresp import log_success_response_with_affiliation
from myuw.logger.session_log import log_session
from myuw.views.rest_dispatch import invalid_session
from myuw.dao.uwemail import get_email_forwarding_for_current_user
from myuw.dao.card_display_dates import get_card_visibilty_date_values


logger = logging.getLogger(__name__)
LOGOUT_URL = "/user_logout"


@login_required
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def index(request,
          year=None,
          quarter=None,
          summer_term=None):

    timer = Timer()
    netid = UserService().get_user()
    if not netid:
        log_invalid_netid_response(logger, timer)
        return invalid_session()

    if _is_mobile(request):
        # On mobile devices, all students get the current myuw.  Non-students
        # are sent to the legacy site.
        try:
            if not is_student():
                logger.info("%s not a student, redirect to legacy!" % netid)
                return redirect_to_legacy_site()
        except Exception:
            log_exception(logger,
                          '%s is_student' % netid,
                          traceback.format_exc())
            logger.info("%s, redirected to legacy!" % netid)
            return redirect_to_legacy_site()

    else:
        if is_oldmyuw_user():
            return redirect_to_legacy_site()

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
    try:
        my_uwemail_forwarding = get_email_forwarding_for_current_user()
        if my_uwemail_forwarding.is_active():
            c_user = context["user"]
            try:
                (c_user['email_forward_url'],
                 c_user['email_forward_title'],
                 c_user['email_forward_icon']) = get_service_url_for_address(
                     my_uwemail_forwarding.fwd)
            except EmailServiceUrlException:
                c_user['login_url'] = None
                c_user['title'] = None
                c_user['icon'] = None
                logger.info('No Mail Url: %s' % (
                    my_uwemail_forwarding.fwd))

    except Exception:
        log_exception(logger,
                      'get_email_forwarding_for_current_user',
                      traceback.format_exc())
        pass

    context["user"]["netid"] = netid
    if year is None or quarter is None:
        cur_term = get_current_quarter(request)
        if cur_term is None:
            context["err"] = "No current quarter data!"
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter
    else:
        pass

    context['enabled_features'] = getattr(
        settings, "MYUW_ENABLED_FEATURES", [])

    log_success_response_with_affiliation(logger, timer, request)
    return render(request, "index.html", context)


def _is_mobile(request):
    user_agent = request.META.get("HTTP_USER_AGENT")

    if not user_agent:
        return False

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

    # Redirects to weblogin logout page
    return HttpResponseRedirect(LOGOUT_URL)
