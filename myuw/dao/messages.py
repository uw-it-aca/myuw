import csv
import os
import datetime
import bleach
from dateutil.parser import parse
from django.conf import settings
from myuw.dao.term import get_comparison_date
from myuw.dao import is_netid_in_list, get_netid_of_current_user
from myuw.models import BannerMessage
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.affiliation_data import get_data_for_affiliations
from userservice.user import UserService
from authz_group import Group

MESSAGE_ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + ["h1", "h2", "h3", "h4"]


def get_current_messages(request):
    current_date = get_comparison_date(request)
    affiliations = get_all_affiliations(request)

    messages = get_data_for_affiliations(model=BannerMessage,
                                         affiliations=affiliations,
                                         start__lte=current_date,
                                         end__gte=current_date,
                                         is_published=True)

    filtered = []
    user = UserService().get_user()
    g = Group()
    for message in messages:
        if message.group_id:
            if not g.is_member_of_group(user, message.group_id):
                continue
        filtered.append(message)
    return filtered


def clean_html(input):
    return bleach.clean(input, tags=MESSAGE_ALLOWED_TAGS)
