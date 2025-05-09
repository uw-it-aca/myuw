# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from restclients_core.exceptions import DataFailureException
from myuw.dao import is_action_disabled
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.emaillink import get_service_url_for_address
from myuw.dao.exceptions import (
    EmailServiceUrlException, BlockedNetidErr)
from myuw.dao.gws import in_myuw_test_access_group
from myuw.dao.quicklinks import get_quicklink_data
from myuw.dao.card_display_dates import get_card_visibilty_date_values
from myuw.dao.persistent_messages import BannerMessage
from myuw.dao.pws import is_student
from myuw.dao.term import add_term_data_to_context
from myuw.dao.user import get_updated_user, not_existing_user
from myuw.dao.user_pref import get_migration_preference
from myuw.dao.uwnetid import get_email_forwarding_for_current_user
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_page_view, log_exception
from myuw.logger.session_log import (
    log_session, is_native, log_session_end)
from myuw.util.settings import (
    get_google_search_key, get_google_analytics_key, get_django_debug,
    get_logout_url, no_access_check)
from myuw.views import prefetch_resources, get_enabled_features
from myuw.views.error import no_access
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)


def page(request,
         template,
         context=None,
         prefetch=True,
         add_quicklink_context=False):
    if context is None:
        context = {}

    timer = Timer()
    try:
        user = get_updated_user(request)
    except DataFailureException as ex:
        log_exception(logger, "PWS error", traceback)
        if ex.status == 404:
            return render(request, '403.html', status=403)
        return render(request, '500.html', status=500)

    try:
        if not can_access_myuw(request):
            return no_access()
    except DataFailureException:
        log_exception(logger, "GWS error", traceback)
        return render(request, '500.html', status=500)

    netid = user.uwnetid
    context["user"] = {
        "netid": netid,
        "isHybrid": is_native(request),
    }

    if prefetch:
        # Some pages need to prefetch before this point
        failure = try_prefetch(request, template, context)
        if failure:
            return failure

    try:
        affiliations = get_all_affiliations(request)
    except BlockedNetidErr:
        return render(request, '400.html', status=400)
    except DataFailureException:
        log_exception(logger, "Failed to get_all_affiliations", traceback)
        return render(request, '500.html', status=500)

    user_pref = get_migration_preference(request)
    log_session(request)

    context["user"]["session_key"] = request.session.session_key
    context["home_url"] = "/"
    context["err"] = None
    context["user"]["affiliations"] = affiliations
    banner_messages = []
    try:
        banner_messages = BannerMessage(request).get_message_json()
    except Exception:
        log_exception(logger, "BannerMessage error", traceback)

    context["banner_messages"] = banner_messages
    context["display_onboard_message"] = user_pref.display_onboard_message
    context["display_pop_up"] = user_pref.display_pop_up
    context["disable_actions"] = is_action_disabled()

    _add_email_forwarding(request, context)

    try:
        context["card_display_dates"] = get_card_visibilty_date_values(request)
        add_term_data_to_context(request, context)
    except DataFailureException:
        log_exception(logger, "SWS term data error", traceback)

    context['enabled_features'] = get_enabled_features()

    context['google_search_key'] = get_google_search_key()
    context['google_analytics_key'] = get_google_analytics_key()
    context['google_tracking_enabled'] = not get_django_debug()

    if add_quicklink_context:
        _add_quicklink_context(request, context)

    log_page_view(timer, request, template)
    return render(request, template, context)


def try_prefetch(request, template, context):
    try:
        prefetch_resources(
            request,
            prefetch_migration_preference=True,
            prefetch_enrollment=(True if is_student(request) else False),
            prefetch_group=True,
            prefetch_instructor=True,
            prefetch_sws_person=(True if is_student(request) else False)
        )
    except DataFailureException:
        log_exception(logger, "prefetch error", traceback)
        context["webservice_outage"] = True
        return render(request, template, context)
    return


@login_required
def logout(request):
    log_session_end(request)
    django_logout(request)  # clear the session data

    if is_native(request):
        return HttpResponse()

    # Redirects to authN service logout page
    return HttpResponseRedirect(get_logout_url())


def _add_quicklink_context(request, context):
    link_data = get_quicklink_data(request)

    for key in link_data:
        context[key] = link_data[key]


def can_access_myuw(request):
    return (no_access_check() or in_myuw_test_access_group(request))


def _add_email_forwarding(request, context):
    my_uwemail_forwarding = get_email_forwarding_for_current_user(request)
    c_user = context["user"]
    if my_uwemail_forwarding and my_uwemail_forwarding.is_active():
        try:
            c_user['email_forward_url'] = get_service_url_for_address(
                my_uwemail_forwarding.fwd)
            return
        except EmailServiceUrlException:
            logger.error('No email url for {}'.format(
                my_uwemail_forwarding.fwd))
            return  # MUWM-4700
    c_user['email_forward_url'] = None
    c_user['email_error'] = True
