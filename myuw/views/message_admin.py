# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
import logging
from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dateutil.parser import parse
from myuw.models import BannerMessage
from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template
from myuw.logger.logresp import log_info
from myuw.dao import get_netid_of_original_user
from myuw.dao.term import get_comparison_datetime_with_tz
from myuw.dao.messages import clean_html


logger = logging.getLogger(__name__)


@login_required
@admin_required
def manage_messages(request):
    context = {}
    if request.POST:
        if _save_new_message(request, context):
            return redirect('myuw_manage_messages')
        if _delete_message(request):
            return redirect('myuw_manage_messages')
        if _handle_publish(request):
            return redirect('myuw_manage_messages')

    messages = BannerMessage.objects.all().order_by('-end', '-start')

    used_now = get_comparison_datetime_with_tz(request)
    for message in messages:
        if message.start <= used_now <= message.end:
            message.is_current = True

    context['now'] = used_now
    context['messages'] = messages
    set_admin_wrapper_template(context)

    return render(request, "admin/messages.html", context)


def _handle_publish(request):
    try:
        message = BannerMessage.objects.get(pk=request.POST.get('pk'))
    except BannerMessage.DoesNotExist:
        return False

    if 'publish' == request.POST['action']:
        message.is_published = True
    elif 'unpublish' == request.POST['action']:
        message.is_published = False
    else:
        return False

    message.save()
    return True


def _delete_message(request):
    if 'delete' != request.POST['action']:
        return False

    message = BannerMessage.objects.get(pk=request.POST['pk'])
    title = message.message_title

    message.delete()
    log_info(logger, {'msg': "Deleted message (Title: {})".format(title)})
    return True


def _save_new_message(request, context):
    if 'save' != request.POST['action']:
        return False

    has_error = False

    def _get_string(string):
        return string.strip()

    def _get_date(name):
        datetimestr = (_get_string(request.POST.get(name, '')) + " " +
                       _get_string(request.POST.get("{}_time".format(name),
                                                    '')))
        try:
            return parse(datetimestr)
        except ValueError:
            return None

    start = _get_date('start')
    end = _get_date('end')

    title = clean_html(request.POST.get('title', ''))
    body = clean_html(request.POST.get('message', ''))

    if not start:
        has_error = True
        context['start_error'] = True

    if not end:
        has_error = True
        context['end_error'] = True

    if has_error:
        context['has_error'] = True
        context['input'] = request.POST

    else:
        affiliation = request.POST.get('affiliation', None)
        pce = None
        if 'pce' == request.POST.get('pce', ''):
            pce = True

        is_published = False
        if request.POST.get('is_published', False):
            is_published = True
        group_id = request.POST.get('group_id', None)
        added_by = get_netid_of_original_user()
        BannerMessage.objects.create(start=start,
                                     end=end,
                                     added_by=added_by,
                                     message_title=title,
                                     campus=request.POST.get('campus', None),
                                     affiliation=affiliation,
                                     pce=pce,
                                     group_id=group_id,
                                     is_published=is_published,
                                     message_body=body)

        log_info(logger, {'msg': "Saved message (Title: {})".format(title)})
        return True

    return False
