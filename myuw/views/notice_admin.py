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
    #
    # messages = BannerMessage.objects.all().order_by('-end', '-start')
    #
    # used_now = timezone.make_aware(get_comparison_datetime(request))
    # for message in messages:
    #     if message.start <= used_now <= message.end:
    #         message.is_current = True
    #
    # context['now'] = used_now
    # context['messages'] = messages
    set_admin_wrapper_template(context)

    return render(request, "admin/notices.html", context)


def _save_new_notice(request, context):
    if 'save' != request.POST['action']:
        return False

    has_error = False

    title = clean_html(request.POST.get('title'))
    content = clean_html(request.POST.get('content'))
    start_date = _get_datetime(request.POST.get('start_date'))
    end_date = _get_datetime(request.POST.get('end_date'))

    notice_type = request.POST.get('notice_type')
    notice_category = request.POST.get('notice_category')

    campus_list = request.POST.getlist('campus')
    affil_list = request.POST.getlist('affil')

    notice = MyuwNotice(title=title,
                        content=content,
                        notice_type=notice_type,
                        notice_category=notice_category)
    if start_date:
        notice.start = start_date
    if end_date:
        notice.end = end_date

    for campus in campus_list:
        setattr(notice, campus, True)

    for affil in affil_list:
        setattr(notice, affil, True)

    notice.save()


def _get_datetime(dt_string):
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
    except ValueError:
        dt = None
    return dt
