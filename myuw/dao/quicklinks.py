# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import logging
import os
import traceback
from myuw.models import VisitedLinkNew, CustomLink, HiddenLink
from myuw.dao import log_err
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.affiliation_data import get_data_for_affiliations
from myuw.dao.user import get_user_model


RECENT_LINKS_DISPLAY_LIMIT = 5
CACHED_LABEL_DATA = {}
logger = logging.getLogger(__name__)


def get_quicklink_data(request):
    affiliations = get_all_affiliations(request)
    data = {}
    # MUWM-4955
    existing_link_urls = set()
    existing_custom_links = []
    user = get_user_model(request)
    custom_links = CustomLink.objects.filter(user=user).order_by('pk')
    for link in custom_links:
        existing_custom_links.append(
            {'url': link.url, 'label': link.label, 'id': link.pk})
        existing_link_urls.add(link.url)

    data['custom_links'] = existing_custom_links

    # user's deletion of default links
    hidden = HiddenLink.objects.filter(user=user)
    saved_def_link_urls = set()
    for link in hidden:
        saved_def_link_urls.add(link.url)

    default_links = []
    default = _get_default_links(affiliations)
    for link in default:
        if (link["url"] not in existing_link_urls and
                link["url"] not in saved_def_link_urls):
            default_links.append({"url": link["url"], "label": link["label"]})
            existing_link_urls.add(link["url"])

    data["default_links"] = default_links

    recents = []
    recent_links = VisitedLinkNew.recent_for_user(user)
    for link in recent_links:
        added = link.url in existing_link_urls
        recents.append({'added': added,
                        'url': link.url,
                        'label': get_link_label(link),
                        'id': link.pk})

    data['recent_links'] = recents[:RECENT_LINKS_DISPLAY_LIMIT]

    return data


def get_link_label(link):
    if 'data' not in CACHED_LABEL_DATA:
        data = {}
        path = os.path.join(os.path.dirname(__file__), '..', 'data',
                            "custom_link_labels.csv")
        with open(path, 'r', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data[row['url']] = row['label']
        CACHED_LABEL_DATA['data'] = data

    return CACHED_LABEL_DATA['data'].get(link.url, link.label)


def _get_default_links(affiliations):
    data = get_data_for_affiliations(file='quicklinks.csv',
                                     affiliations=affiliations,
                                     unique=lambda x: x['URL'])

    defaults = []
    for link in data:
        defaults.append({'url': link['URL'], 'label': link['Label']})

    return defaults


def add_custom_link(request, url, link_label=None):
    try:
        obj, created = CustomLink.objects.update_or_create(
            user=get_user_model(request), url=url, label=link_label)
        return obj
    except Exception:
        log_err(
            logger, f"add_custom_link({url}, {link_label})", traceback, request
        )
    return None


def delete_custom_link(request, link_id):
    try:
        link = get_custom_link_by_id(request, link_id)
        return link.delete()
    except Exception:
        log_err(
            logger, f"delete_custom_link({link_id})", traceback, request)
    return None


def edit_custom_link(request, link_id, new_url, new_label=None):
    try:
        link = get_custom_link_by_id(request, link_id)
        link.url = new_url
        if new_label is not None and len(new_label):
            link.label = new_label
        link.save()
        return link
    except Exception:
        log_err(
            logger, f"edit_custom_link({link_id}, {new_url}, {new_label})",
            traceback, request)
    return None


def get_custom_link_by_id(request, link_id):
    return CustomLink.objects.get(pk=link_id, user=get_user_model(request))


def get_custom_link_by_url(request, url):
    return CustomLink.objects.get(user=get_user_model(request), url=url)


def add_hidden_link(request, url):
    try:
        logger.debug(f"add_hidden_link({url})")
        obj, created = HiddenLink.objects.update_or_create(
            user=get_user_model(request), url=url)
        return obj
    except Exception:
        log_err(logger, f"add_hidden_link({url})", traceback, request)
    return None


def delete_hidden_link(request, link_id):
    try:
        logger.error(f"delete_hidden_link({link_id})")
        link = get_hidden_link_by_id(request, link_id)
        return link.delete()
    except Exception:
        log_err(logger, f"delete_hidden_link({link_id})",
                traceback, request)
    return None


def get_hidden_link_by_id(request, link_id):
    return HiddenLink.objects.get(pk=link_id, user=get_user_model(request))


def get_hidden_link_by_url(request, url):
    return HiddenLink.objects.get(user=get_user_model(request), url=url)


def get_recent_link_by_id(request, link_id):
    return VisitedLinkNew.objects.get(pk=link_id,
                                      user=get_user_model(request))
