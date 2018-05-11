from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template
from myuw.dao.messages import clean_html
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import logging
from myuw.models.myuw_notice import MyuwNotice
from datetime import datetime


logger = logging.getLogger(__name__)


@login_required
@admin_required('MYUW_ADMIN_GROUP')
def manage_notices(request):
    context = {}
    if request.POST:
        if _save_new_notice(request, context):
            return redirect('myuw_manage_notices')
    set_admin_wrapper_template(context)

    return render(request, "admin/notices.html", context)


def _save_new_notice(request, context):
    form_action = request.POST.get('action')
    if 'save' != form_action:
        return False

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
        return True
    else:
        return False


def _get_datetime(dt_string):
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
    except ValueError:
        dt = None
    return dt
