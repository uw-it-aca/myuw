import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao import get_user_model, get_netid_of_current_user,\
    get_netid_of_original_user
from myuw.views import prefetch_resources
from myuw.models import VisitedLinkNew
from urllib import unquote
import os
import re


logger = logging.getLogger(__name__)
ignored_links = set()


def outbound_link(request):
    url = request.GET.get('u', '')

    if not re.match('^https?://', url):
        return HttpResponseRedirect("/")

    if is_link_of_interest(url):
        save_visited_link(request)

    return HttpResponseRedirect(url)


def save_visited_link(request):
    url = request.GET.get('u', '')
    label = request.GET.get('l', None)

    netid = get_netid_of_current_user(request)
    if not netid:
        return

    try:
        user = get_user_model(request)
    except IntegrityError:
        return

    original = get_netid_of_original_user()
    prefetch_resources(request, prefetch_group=True)

    if label:
        label = unquote(label)

    affiliations = get_all_affiliations(request)
    link_data = {"user": user,
                 "url": url,
                 "label": label,
                 "is_anonymous": not (netid == original),
                 "is_student": affiliations.get('student', False),
                 "is_undegrad": affiliations.get('undergrad', False),
                 "is_grad_student": affiliations.get('grad', False),
                 "is_employee": affiliations.get('employee', False),
                 "is_faculty": affiliations.get('faculty', False),
                 "is_seattle": affiliations.get('seattle', False),
                 "is_tacoma": affiliations.get('tacoma', False),
                 "is_bothell": affiliations.get('bothell', False),
                 "is_pce": affiliations.get('pce', False),
                 "is_student_employee": affiliations.get('stud_employee',
                                                         False)
                 }
    VisitedLinkNew.objects.create(**link_data)


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
