import re
import logging
import traceback
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
from django.conf import settings
from userservice.user import UserService
from myuw.dao.term import get_current_quarter
from myuw.dao.pws import is_student
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.user import is_oldmyuw_user, get_netid_of_current_user,\
    is_oldmyuw_mobile_user
from myuw.dao.emaillink import get_service_url_for_address
from myuw.dao.exceptions import EmailServiceUrlException
from myuw.logger.timer import Timer
from myuw.logger.logback import log_exception
from myuw.logger.logresp import log_invalid_netid_response
from myuw.logger.logresp import log_success_response_with_affiliation
from myuw.logger.session_log import log_session
from myuw.views.error import invalid_session
from myuw.dao.uwemail import get_email_forwarding_for_current_user
from myuw.dao.card_display_dates import get_card_visibilty_date_values
from myuw.views import prefetch_resources
from restclients.exceptions import DataFailureException


logger = logging.getLogger(__name__)
LOGOUT_URL = "/user_logout"


def page(request,
         context={},
         template='index.html'):
    timer = Timer()
    netid = get_netid_of_current_user()
    if not netid:
        log_invalid_netid_response(logger, timer)
        return invalid_session()
    context["user"] = {
        "netid": netid,
        "session_key": request.session.session_key,
     }

    try:
        prefetch_resources(request,
                           prefetch_email=True,
                           prefetch_enrollment=True)
    except DataFailureException:
        log_exception(logger,
                      "prefetch_resources",
                      traceback.format_exc())
        context["webservice_outage"] = True
        return render(request, template, context)
    log_session(netid, request.session.session_key, request)

    if _is_mobile(request):
        # On mobile devices, all students get the current myuw.  Non-students
        # are sent to the legacy site.
        try:
            if is_oldmyuw_mobile_user():
                logger.info("mobile user %s, redirect to legacy!" % netid)
                return redirect_to_legacy_site()
        except Exception:
            log_exception(logger,
                          '%s is_oldmyuw_mobile_user' % netid,
                          traceback.format_exc())
            logger.info("%s, redirected to legacy!" % netid)
            return redirect_to_legacy_site()

    else:
        if is_oldmyuw_user():
            return redirect_to_legacy_site()

    context["home_url"] = "/"
    context["err"] = None
    context["user"]["affiliations"] = get_all_affiliations(request)

    context["card_display_dates"] = get_card_visibilty_date_values(request)
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

    if ('year' not in context or context['year'] is None or
            'quarter' not in context and context['quarter'] is None):
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
    return render(request, template, context)


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
