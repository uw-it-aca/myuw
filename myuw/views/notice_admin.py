from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template
from myuw.dao.messages import clean_html
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import logging
from myuw.models.myuw_notice import MyuwNotice
from datetime import datetime
from myuw.dao.term import get_comparison_datetime


logger = logging.getLogger(__name__)


@login_required
@admin_required('MYUW_ADMIN_GROUP')
def create_notice(request):
    context = {}
    if request.POST:
        if _save_notice(request, context):
            return redirect('myuw_manage_notices')
    set_admin_wrapper_template(context)
    context['action'] = "save"
    return render(request, "admin/notice_edit.html", context)


@login_required
@admin_required('MYUW_ADMIN_GROUP')
def edit_notice(request, notice_id):
    context = {}
    set_admin_wrapper_template(context)
    if request.POST:
        _save_notice(request, context, notice_id)
    notice = _get_notice_by_id(notice_id)
    context['notice'] = notice
    context['action'] = "edit"
    return render(request, "admin/notice_edit.html", context)


@login_required
@admin_required('MYUW_ADMIN_GROUP')
def list_notices(request):
    context = {}
    set_admin_wrapper_template(context)
    now = get_comparison_datetime(request)
    notices = MyuwNotice.objects.filter(end__gte=now).order_by('start', 'end')
    context['notices'] = notices
    return render(request, "admin/notice_list.html", context)


def _get_notice_by_id(notice_id):
    notice = MyuwNotice.objects.get(id=notice_id)
    return notice


def _get_notice_data(request, context):
    pass


def _edit_notice(request, context):
    pass


def _save_notice(request, context, notice_id=None):
    form_action = request.POST.get('action')

    has_error = False

    start_date = None
    end_date = None
    try:
        start_date = _get_datetime(request.POST.get('start_date'))
    except TypeError:
        has_error = True
        context['start_error'] = True

    try:
        end_date = _get_datetime(request.POST.get('end_date'))
    except TypeError:
        has_error = True
        context['end_error'] = True

    try:
        if end_date < start_date:
            has_error = True
            context['date_error'] = True
    except TypeError:
        pass

    notice_type = request.POST.get('notice_type')
    notice_category = request.POST.get('notice_category')
    if notice_type is None:
        has_error = True
        context['type_error'] = True
    if notice_category is None:
        has_error = True
        context['category_error'] = True

    title = None
    content = None
    try:
        title = clean_html(request.POST.get('title'))
    except TypeError:
        has_error = True
        context['title_error'] = True
    try:
        content = clean_html(request.POST.get('content'))
    except TypeError:
        has_error = True
        context['content_error'] = True

    campus_list = request.POST.getlist('campus')
    affil_list = request.POST.getlist('affil')

    if not has_error:
        if form_action == "save":
            notice = MyuwNotice(title=title,
                                content=content,
                                notice_type=notice_type,
                                notice_category=notice_category,
                                start=start_date,
                                end=end_date)
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

            # reset filters
            fields = MyuwNotice._meta.get_fields()
            for field in fields:
                if "is_" in field.name:
                    setattr(notice, field.name, False)

            for campus in campus_list:
                setattr(notice, campus, True)

            for affil in affil_list:
                setattr(notice, affil, True)
            notice.save()

        return True
    else:
        return False


def _get_datetime(dt_string):
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
    except ValueError:
        dt = None
    return dt
