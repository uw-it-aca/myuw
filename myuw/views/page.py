import re
import logging
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from restclients_core.exceptions import DataFailureException
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.emaillink import get_service_url_for_address
from myuw.dao.exceptions import EmailServiceUrlException
from myuw.dao.quicklinks import get_quicklink_data
from myuw.dao.uwemail import get_email_forwarding_for_current_user
from myuw.dao.card_display_dates import get_card_visibilty_date_values
from myuw.dao.messages import get_current_messages
from myuw.dao.term import add_term_data_to_context
from myuw.dao.user import is_oldmyuw_user, get_netid_of_current_user
from myuw.logger.timer import Timer
from myuw.logger.logback import log_exception
from myuw.logger.logresp import log_invalid_netid_response,\
    log_success_response_with_affiliation
from myuw.logger.session_log import log_session
from myuw.util.settings import get_google_search_key,\
    get_legacy_url, get_logout_url
from myuw.views import prefetch_resources, get_enabled_features
from myuw.views.error import invalid_session



logger = logging.getLogger(__name__)


def page(request,
         context=None,
         template='index.html',
         prefetch=True,
         add_quicklink_context=False):

    if context is None:
        context = {}

    timer = Timer()
    netid = get_netid_of_current_user()
    if not netid:
        log_invalid_netid_response(logger, timer)
        return invalid_session()
    context["user"] = {
        "netid": netid,
        "session_key": request.session.session_key,
     }

    if prefetch:
        # Some pages need to prefetch before this point
        failure = try_prefetch(request)
        if failure:
            return failure
    log_session(netid, request.session.session_key, request)

    if is_oldmyuw_user():
        return redirect_to_legacy_site()

    context["home_url"] = "/"
    context["err"] = None
    affiliations = get_all_affiliations(request)
    context["user"]["affiliations"] = affiliations

    context["banner_messages"] = get_current_messages(request)
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

    add_term_data_to_context(request, context)

    context['enabled_features'] = get_enabled_features()

    context['google_search_key'] = get_google_search_key()

    if add_quicklink_context:
        _add_quicklink_context(affiliations, context)

    log_success_response_with_affiliation(logger, timer, request)
    return render(request, template, context)


def try_prefetch(request):
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
    return


def redirect_to_legacy_site():
    return HttpResponseRedirect(get_legacy_url())


def logout(request):
    # Expires current myuw session
    django_logout(request)

    # Redirects to authN service logout page
    return HttpResponseRedirect(get_logout_url())


def _add_quicklink_context(affiliations, context):
    link_data = get_quicklink_data(affiliations)

    for key in link_data:
        context[key] = link_data[key]
