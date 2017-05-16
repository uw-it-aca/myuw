from myuw.models import BannerMessage
from myuw.logger.logback import log_info
from userservice.user import UserService
from authz_group import Group
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import bleach
import re
import logging


logger = logging.getLogger(__name__)


@login_required
def manage_messages(request):

    # XXX - replace all of this once teaching page is merged and we can use
    # @admin_required('MYUW_ADMIN_GROUP')
    user_service = UserService()
    user_service.get_user()
    override_error_username = None
    override_error_msg = None
    # Do the group auth here.

    if not hasattr(settings, "USERSERVICE_ADMIN_GROUP"):
        print "You must have a group defined as your admin group."
        print 'Configure that using USERSERVICE_ADMIN_GROUP="foo_group"'
        raise Exception("Missing USERSERVICE_ADMIN_GROUP in settings")

    actual_user = user_service.get_original_user()
    if not actual_user:
        raise Exception("No user in session")

    g = Group()
    group_name = settings.USERSERVICE_ADMIN_GROUP
    is_admin = g.is_member_of_group(actual_user, group_name)
    if is_admin is False:
        return render(request, 'no_access.html', {})

    context = {}
    if request.POST:
        if _save_new_message(request, context):
            return redirect('myuw_manage_messages')
        if _delete_message(request):
            return redirect('myuw_manage_messages')

    one_week_past = timezone.now() - timedelta(days=7)
    messages = BannerMessage.objects.filter(end__gte=one_week_past)

    context['messages'] = messages

    return render(request, "message_admin/messages.html", context)


def _delete_message(request):
    if 'delete' != request.POST['action']:
        return False

    message = BannerMessage.objects.get(pk=request.POST['pk'])
    title = message.message_title

    message.delete()
    log_info(logger, "Message deleted.  Title: %s" % title)
    return True


def _clean_html(input):
    return bleach.clean(input)


def _save_new_message(request, context):
    if 'save' != request.POST['action']:
        return False

    has_error = False

    def _get_string(string):
        return string.strip()

    def _get_date(string):
        string = _get_string(string)
        try:
            return datetime.strptime(string, "%Y-%m-%d").date()
        except ValueError:
            return

    start = _get_date(request.POST.get('start', ''))
    end = _get_date(request.POST.get('end', ''))
    title = _clean_html(request.POST.get('title', ''))
    body = _clean_html(request.POST.get('message', ''))

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

        added_by = UserService().get_original_user()
        BannerMessage.objects.create(start=start,
                                     end=end,
                                     added_by=added_by,
                                     message_title=title,
                                     campus=request.POST.get('campus', None),
                                     affiliation=affiliation,
                                     pce=pce,
                                     message_body=body)

        log_info(logger, "Message saved.  Title: %s" % title)
        return True

    return False
