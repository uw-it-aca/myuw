from myuw.models import BannerMessage
from myuw.views import admin_required, set_admin_wrapper_template
from myuw.logger.logback import log_info
from myuw.dao.term import get_comparison_datetime
from myuw.dao.messages import clean_html
from userservice.user import UserService
from authz_group import Group
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import re
import logging


logger = logging.getLogger(__name__)


@login_required
@admin_required('MYUW_ADMIN_GROUP')
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

    used_now = timezone.make_aware(get_comparison_datetime(request))
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
    log_info(logger, "Message deleted.  Title: %s" % title)
    return True


def _save_new_message(request, context):
    if 'save' != request.POST['action']:
        return False

    has_error = False

    def _get_string(string):
        return string.strip()

    def _get_date(name):
        datetimestr = (_get_string(request.POST.get(name, '')) + " " +
                       _get_string(request.POST.get("%s_time" % name, '')))
        try:
            return datetime.strptime(datetimestr, "%Y-%m-%d %H:%M")
        except ValueError:
            return

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
        added_by = UserService().get_original_user()
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

        log_info(logger, "Message saved.  Title: %s" % title)
        return True

    return False
