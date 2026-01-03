# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import nh3
import traceback
import unicodedata
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from myuw.dao.term import DEFAULT_TZ
from myuw.models.myuw_notice import (
    MyuwNotice, start_week_range, duration_range)
from myuw.logger.logresp import log_info, log_exception
from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template

logger = logging.getLogger(__name__)
ALLOWED_TAGS = {
    'b', 'br', 'em', 'p', 'span', 'a', 'img', 'i', 'li', 'ol', 'strong', 'ul'
}
ALLOWED_ATTS = {
    '*': {'class', 'style', 'title'},
    'a': {'href', 'rel'},
    'img': {'alt'}
}


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
    start_week = 0
    duration = 0
    terms = None

    start_date = _get_datetime(request.POST.get('start_date'))
    end_date = _get_datetime(request.POST.get('end_date'))
    if start_date or end_date:
        if start_date is None:
            has_error = True
            context['start_error'] = True
            log_info(
                logger, {'err': 'Invalid start_date'})

        if end_date is None:
            has_error = True
            context['end_error'] = True
            log_info(
                logger, {'err': 'Invalid end_date'})

        if start_date and end_date and end_date < start_date:
            has_error = True
            context['date_error'] = True
            log_info(
                logger,
                {'err': 'end_date is before start_date',
                 'start_date': start_date,
                 'end_date': end_date})

    else:
        start_week = _get_integer(request.POST.get('start_week'))
        if start_week not in start_week_range:
            has_error = True
            context['start_week_error'] = True
            log_info(logger, {'err': 'Invalid start_week'})

        duration = _get_integer(request.POST.get('duration'))
        if duration not in duration_range:
            has_error = True
            context['duration_error'] = True
            log_info(logger, {'err': 'Invalid duration'})

        terms = request.POST.getlist('terms')
        if not terms or len(terms) == 0:
            has_error = True
            context['terms_error'] = True
            log_info(logger, {'err': 'Invalid terms'})

    notice_type = request.POST.get('notice_type')
    if notice_type is None:
        has_error = True
        context['type_error'] = True
        log_info(logger, {'err': 'Invalid notice_type'})

    notice_category = request.POST.get('notice_category')
    if notice_category is None:
        has_error = True
        context['category_error'] = True
        log_info(logger, {'err': 'Invalid notice_category'})

    try:
        is_critical = request.POST.get('critical') is not None
    except (KeyError, TypeError):
        is_critical = False

    try:
        title = _get_html(request.POST.get('title'))
    except Exception as ex:
        title = None
        log_info(logger, {'err': ex, 'msg': 'Invalid title'})
    if title is None or len(title) == 0:
        has_error = True
        context['title_error'] = True

    try:
        content = _get_html(request.POST.get('content'))
        logger.debug({'content': content})
    except Exception as ex:
        content = None
        log_info(logger, {'err': ex, 'msg': 'Invalid content'})
    if content is None or len(content) == 0:
        has_error = True
        context['content_error'] = True

    target_group = request.POST.get('target_group')
    if target_group is not None and len(target_group):
        target_group = target_group.strip()

    campus_list = request.POST.getlist('campus')
    affil_list = request.POST.getlist('affil')
    if has_error:
        context['has_error'] = has_error
        return False

    if form_action == "save":
        notice = MyuwNotice(title=title,
                            content=content,
                            notice_type=notice_type,
                            notice_category=notice_category,
                            is_critical=is_critical,
                            target_group=target_group)

        if (start_week in start_week_range and
                duration in duration_range and
                terms and len(terms) > 0):
            notice.start_week = start_week
            notice.duration = duration
            for term in terms:
                setattr(notice, term, True)

        if start_date and end_date:
            notice.start = start_date
            notice.end = end_date

        for campus in campus_list:
            setattr(notice, campus, True)

        for affil in affil_list:
            setattr(notice, affil, True)
        try:
            notice.save()
            log_info(logger, {'Saved notice': notice})
            return True
        except Exception:
            log_exception(logger, "save_notice", traceback)
            context['sql_error'] = True

    elif form_action == "edit":
        notice = MyuwNotice.objects.get(id=notice_id)
        notice.title = title
        notice.content = content
        notice.notice_type = notice_type
        notice.notice_category = notice_category
        notice.start = start_date
        notice.end = end_date
        notice.start_week = start_week
        notice.duration = duration
        notice.target_group = target_group

        # reset filters
        fields = MyuwNotice._meta.get_fields()
        for field in fields:
            if "is_" in field.name:
                setattr(notice, field.name, False)
            elif "not_" in field.name:
                setattr(notice, field.name, False)

        if terms and len(terms) > 0:
            for att in terms:
                setattr(notice, att, True)

        for campus in campus_list:
            setattr(notice, campus, True)

        for affil in affil_list:
            setattr(notice, affil, True)

        notice.is_critical = is_critical
        try:
            notice.save()
            log_info(logger, {'Edited notice': notice})
            return True
        except Exception:
            log_exception(logger, "edit_notice", traceback)
            context['sql_error'] = True

    return False


def _get_datetime(dt_string):
    if dt_string and len(dt_string) > 0:
        try:
            dt = parse(dt_string)
            if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
                return dt.replace(tzinfo=DEFAULT_TZ)
            return dt
        except Exception as ex:
            log_info(
                logger,
                {'err': ex, 'msg': "_get_datetime({})".format(dt_string)})
    return None


def _get_integer(str):
    if str and len(str):
        try:
            value = int(str)
            return value
        except Exception as ex:
            log_info(
                logger,
                {'err': ex, 'msg': "_get_integer({})".format(str)})
    return 100


def _get_html(value):
    try:
        content = nh3.clean(
            remove_curly_quotes(value),   # MUWM-5374
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTS,
            link_rel=None)
        return unicodedata.normalize("NFKD", content).strip()
        # MUWM-5092
    except TypeError as ex:
        log_info(
            logger, {'err': ex, 'msg': "_get_html({})".format(value)})
        return None


def remove_curly_quotes(html_string):
    # MUWM-5374: Replace curly double and single quotes with straight quotes
    if html_string:
        html_string = html_string.replace("“", '"').replace("”", '"')
        html_string = html_string.replace("‘", "'").replace("’", "'")
    return html_string
