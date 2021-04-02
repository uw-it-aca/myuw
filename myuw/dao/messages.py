# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import os
import datetime
import bleach
from dateutil.parser import parse
from myuw.models import BannerMessage
from myuw.dao import get_netid_of_current_user, is_using_file_dao
from myuw.dao.admin import is_admin
from myuw.dao.gws import gws
from myuw.dao.term import get_comparison_datetime_with_tz
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.affiliation_data import get_data_for_affiliations


MESSAGE_ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + ["span", "h1", "h2",
                                                        "h3", "h4"]
MESSAGE_ALLOWED_ATTRIBUTES = bleach.sanitizer.ALLOWED_ATTRIBUTES.copy()
MESSAGE_ALLOWED_ATTRIBUTES["*"] = ["class", "style", "aria-hidden"]
MESSAGE_ALLOWED_STYLES = ["font-size", "color"]


def get_current_messages(request):
    current_date = get_comparison_datetime_with_tz(request)
    affiliations = get_all_affiliations(request)
    messages = get_data_for_affiliations(model=BannerMessage,
                                         affiliations=affiliations,
                                         start__lte=current_date,
                                         end__gte=current_date,
                                         is_published=True)

    filtered = []
    user_netid = get_netid_of_current_user(request)

    for message in messages:
        if message.group_id:
            if (not is_using_file_dao() and
                    not gws.is_effective_member(message.group_id, user_netid)):
                continue
        filtered.append(message)

    preview_id = request.GET.get('banner', None)
    if preview_id:
        try:
            banner = BannerMessage.objects.get(preview_id=preview_id)
            filtered.append(banner)
        except BannerMessage.DoesNotExist:
            pass
    return filtered


def clean_html(input, additional_tags=None):
    tags = MESSAGE_ALLOWED_TAGS[:]
    if additional_tags:
        tags += additional_tags

    return bleach.clean(input, tags=tags,
                        attributes=MESSAGE_ALLOWED_ATTRIBUTES,
                        styles=MESSAGE_ALLOWED_STYLES)
