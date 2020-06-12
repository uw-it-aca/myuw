import logging
import os
import re
import traceback
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from restclients_core.exceptions import DataFailureException
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao import is_action_disabled, get_netid_of_current_user
from myuw.dao.user import get_user_model
from myuw.models import VisitedLinkNew
from myuw.logger.logresp import log_exception
from myuw.views import prefetch_resources


logger = logging.getLogger(__name__)
ignored_links = set()


@login_required
def outbound_link(request):
    url = request.GET.get('u', '')
    if not re.match('^https?://', url):
        return HttpResponseRedirect("/")

    if (get_netid_of_current_user(request) is not None and
            not is_action_disabled() and
            is_link_of_interest(url)):
        save_visited_link(request)

    return HttpResponseRedirect(url)


def save_visited_link(request):
    url = request.GET.get('u', '')
    label = request.GET.get('l', '')
    user = get_user_model(request)
    prefetch_resources(request, prefetch_group=True, prefetch_sws_person=True)

    if label and len(label) > 0:
        label = unquote(label)
        if len(label) > 50:
            label = label[:50]

    try:
        affiliations = get_all_affiliations(request)
    except DataFailureException as er:
        log_exception(logger, er, traceback)
        return

    link_data = {"user": user,
                 "url": url,
                 "label": label,
                 "is_anonymous": not request.user.is_active,
                 "is_student": affiliations.get('student', False),
                 "is_undegrad": affiliations.get('undergrad', False),
                 "is_grad_student": affiliations.get('grad', False),
                 "is_employee": affiliations.get('employee', False),
                 "is_faculty": affiliations.get('faculty', False),
                 "is_seattle": affiliations.get('seattle', False),
                 "is_tacoma": affiliations.get('tacoma', False),
                 "is_bothell": affiliations.get('bothell', False),
                 "is_pce": affiliations.get('pce', False),
                 "is_intl_stud": affiliations.get('intl_stud', False),
                 "is_student_employee": affiliations.get('stud_employee',
                                                         False)
                 }
    try:
        VisitedLinkNew.objects.create(**link_data)
    except django.db.utils.DataError as ex:
        log_exception(logger, ex, traceback)


def is_link_of_interest(url):
    initialize_ignored_links()

    if url in ignored_links:
        return False
    return True


def initialize_ignored_links():
    if len(ignored_links):
        return

    path = os.path.join(os.path.dirname(__file__),
                        '..', 'data', 'ignored_links.txt')
    with open(path) as handle:
        for line in handle:
            ignored_links.add(line.strip())
