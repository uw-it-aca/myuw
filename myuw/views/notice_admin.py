# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dateutil.parser import parse
from uw_sws import SWS_TIMEZONE
from myuw.dao.messages import clean_html
from myuw.models.myuw_notice import MyuwNotice
from myuw.logger.logresp import log_info
from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template

logger = logging.getLogger(__name__)


@login_required
@admin_required
def create_notice(request):
    context = {}
    if request.POST and _save_notice(request, context):
        return redirect('myuw_manage_notices')
    set_admin_wrapper_template(context)
    context['action'] = "save"
    return render(request, "admin/notice_edit.html", context)


@login_required
@admin_required
def edit_notice(request, notice_id):
    context = {}
    set_admin_wrapper_template(context)
    if request.POST:
        if request.POST.get('action') == "delete":
            MyuwNotice.objects.get(id=notice_id).delete()
            return redirect("myuw_manage_notices")
        else:
            _save_notice(request, context, notice_id)
    notice = _get_notice_by_id(notice_id)
    context['notice'] = notice
    context['action'] = "edit"
    return render(request, "admin/notice_edit.html", context)


@login_required
@admin_required
def list_notices(request):
    context = {}
    set_admin_wrapper_template(context)
    notices = MyuwNotice.objects.order_by('start', 'end')
    context['notices'] = notices
    return render(request, "admin/notice_list.html", context)


def _get_notice_by_id(notice_id):
    notice = MyuwNotice.objects.get(id=notice_id)
    return notice


def _save_notice(request, context, notice_id=None):
    log_info(logger, request.POST)
    form_action = request.POST.get('action')
    if form_action not in ('save', 'edit'):
        return False

    has_error = False

    start_date = None
    end_date = None
    try:
        start_date = _get_datetime(request.POST.get('start_date'))
    except TypeError:
        has_error = True
        context['start_error'] = True
        log_info({'err': 'Missing start_date'})
    if start_date is None:
        has_error = True
        context['start_error'] = True
        log_info({'err': 'Invalid start_date'})

    try:
        end_date = _get_datetime(request.POST.get('end_date'))
    except TypeError:
        has_error = True
        log_info({'err': 'Missing end_date'})
    if end_date is None:
        has_error = True
        context['end_error'] = True
        log_info({'err': 'Invalid end_date'})

    if end_date < start_date:
        has_error = True
        context['date_error'] = True
        log_info(
            {'err': 'end_date is before start_date',
             'start_date': start_date,
             'end_date': end_date})

    notice_type = request.POST.get('notice_type')
    notice_category = request.POST.get('notice_category')
    if notice_type is None:
        has_error = True
        context['type_error'] = True
    if notice_category is None:
        has_error = True
        context['category_error'] = True

    is_critical = request.POST.get('critical') is not None

    title = None
    content = None
    try:
        title = request.POST.get('title')
    except TypeError:
        has_error = True
        context['title_error'] = True
        log_info({'err': 'Invalid title'})

    if title is not None:
        if len(title) == 0:
            has_error = True
            context['title_error'] = True
        else:
            title = title.strip()
    try:
        content = request.POST.get('content')
    except TypeError:
        has_error = True
        context['content_error'] = True
        log_info({'err': 'Invalid content'})

    if content is not None and len(content) == 0:
        has_error = True
        context['content_error'] = True
        log_info({'err': 'Invalid content'})

    target_group = request.POST.get('target_group')
    if target_group is not None:
        target_group = target_group.strip()

    campus_list = request.POST.getlist('campus')
    affil_list = request.POST.getlist('affil')
    if not has_error:
        if form_action == "save":
            notice = MyuwNotice(title=title,
                                content=content,
                                notice_type=notice_type,
                                notice_category=notice_category,
                                is_critical=is_critical,
                                start=start_date,
                                end=end_date,
                                target_group=target_group)
            for campus in campus_list:
                setattr(notice, campus, True)

            for affil in affil_list:
                setattr(notice, affil, True)
            notice.save()

        elif form_action == "edit":
            notice = MyuwNotice.objects.get(id=notice_id)
            notice.title = title
            notice.content = content
            notice.notice_type = notice_type
            notice.notice_category = notice_category
            notice.start = start_date
            notice.end = end_date
            notice.target_group = target_group

            # reset filters
            fields = MyuwNotice._meta.get_fields()
            for field in fields:
                if "is_" in field.name:
                    setattr(notice, field.name, False)

            for campus in campus_list:
                setattr(notice, campus, True)

            for affil in affil_list:
                setattr(notice, affil, True)

            notice.is_critical = is_critical
            notice.save()

        return True
    else:
        context['has_error'] = has_error
        return False


def _get_datetime(dt_string):
    try:
        dt = parse(dt_string)
    except ValueError:
        return None
    return WS_TIMEZONE.localize(dt)
