# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime, timezone
from dateutil import tz
import logging
import traceback
from django.shortcuts import render
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.test.client import RequestFactory
from django.utils.timezone import get_default_timezone
from uw_sws.term import get_term_by_date
from myuw.dao.card_display_dates import get_values_by_date
from myuw.dao.card_display_dates import get_card_visibilty_date_values
from myuw.dao import is_using_file_dao
from myuw.dao.term import (
    get_comparison_datetime, get_default_datetime)
from myuw.dao.user import get_user_model
from myuw.models import SeenRegistration
from myuw.logger.logresp import log_exception
from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template

DATE_KEYS = ['myuw_after_submission', 'myuw_after_last_day', 'myuw_after_reg',
             'myuw_before_finals_end', 'myuw_before_last_day',
             'myuw_before_end_of_reg_display', 'myuw_before_first_day',
             'myuw_before_end_of_first_week', 'myuw_after_eval_start',
             'in_coursevel_fetch_window']
logger = logging.getLogger(__name__)


@login_required
@admin_required
def override(request):
    context = {}
    if request.method == "POST":
        _handle_post(request, context)

    set_admin_wrapper_template(context)
    try:
        add_session_context(request, context)
        add_date_term_info(request, context)

        add_seen_registration_context(request, context)
    except Exception as ex:
        log_exception(logger, "override", traceback)
        context["date_error"] = "Invalid date"
    return render(request, "display_dates/override.html", context)


def _handle_post(request, context):
    if request.POST["date"]:
        try:
            date_obj = datetime.strptime(request.POST["date"],
                                         "%Y-%m-%d %H:%M:%S")
            request.session["myuw_override_date"] = request.POST["date"]
        except Exception as ex:
            try:
                date_obj = datetime.strptime(request.POST["date"],
                                             "%Y-%m-%d")
                request.session["myuw_override_date"] = request.POST["date"]

            except Exception as ex:
                log_exception(logger, "override_date", traceback)
                context["date_error"] = str(ex)

    else:
        if "myuw_override_date" in request.session:
            del request.session["myuw_override_date"]

    for val in DATE_KEYS:
        if val in request.POST:
            if request.POST[val] == "yes":
                request.session[val] = True
            elif request.POST[val] == "no":
                request.session[val] = False
            else:
                if val in request.session:
                    del request.session[val]
        else:
            if val in request.session:
                del request.session[val]


def add_date_term_info(request, context):
    actual_now = get_default_datetime()
    used_now = get_comparison_datetime(request)

    context["actual_now_date"] = str(actual_now)
    context["effective_now_date"] = str(used_now)
    context["is_using_mock_data"] = is_using_file_dao()

    try:
        actual_term = get_term_by_date(actual_now.date())
        context["actual_now_term_year"] = actual_term.year
        context["actual_now_term_quarter"] = actual_term.quarter
    except Exception as ex:
        pass

    try:
        used_term = get_term_by_date(used_now.date())
        context["effective_now_term_year"] = used_term.year
        context["effective_now_term_quarter"] = used_term.quarter
    except Exception as ex:
        pass


def add_session_context(request, context):
    if "myuw_override_date" in request.session:
        context["myuw_override_date"] = request.session["myuw_override_date"]

    for val in DATE_KEYS:
        if val in request.session:
            if request.session[val] is True:
                context["{}_true".format(val)] = True
            else:
                context["{}_false".format(val)] = True
        else:
            context["{}_unset".format(val)] = True

    now_request = RequestFactory().get("/")
    now_request.session = {}
    context["values_used"] = get_card_visibilty_date_values(request)

    used_date = get_default_datetime()
    context["values_now"] = get_values_by_date(used_date, now_request)


def add_seen_registration_context(request, context):
    user = get_user_model(request)

    seen_registrations = SeenRegistration.objects.filter(user=user)
    seen = []

    local_tz = get_default_timezone()

    for reg in seen_registrations:

        seen_date = reg.first_seen_date
        local = seen_date.replace(tzinfo=timezone.utc).astimezone(local_tz)

        seen.append({
            'year': reg.year,
            'quarter': reg.quarter,
            'summer': reg.summer_term,
            'date_seen': local.__str__(),
        })

    context['seen_registrations'] = seen
