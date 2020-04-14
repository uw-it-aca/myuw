import csv
import logging
import os
import traceback
from django.db import transaction, IntegrityError
from myuw.models import VisitedLinkNew, PopularLink, CustomLink, HiddenLink
from myuw.dao import log_err
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.affiliation_data import get_data_for_affiliations
from myuw.dao.user import get_user_model


RECENT_LINKS_DISPLAY_LIMIT = 5
CACHED_LABEL_DATA = {}
logger = logging.getLogger(__name__)


def get_quicklink_data(request):
    data = {}
    affiliations = get_all_affiliations(request)
    # For excluding from the recent list
    existing_list_urls = set()
    custom = []
    custom_lookup = set()
    user = get_user_model(request)
    custom_links = CustomLink.objects.filter(user=user).order_by('pk')
    for link in custom_links:
        existing_list_urls.add(link.url)
        custom_lookup.add(link.url)
        custom.append({'url': link.url, 'label': link.label, 'id': link.pk})

    data['custom_links'] = custom

    popular = []

    popular_links = get_data_for_affiliations(model=PopularLink,
                                              affiliations=affiliations,
                                              unique=lambda x: x.url)
    for link in popular_links:
        added = link.url in custom_lookup
        existing_list_urls.add(link.url)
        popular.append({'added': added,
                        'url': link.url,
                        'label': link.label,
                        'id': link.pk})

    data['popular_links'] = popular

    hidden = HiddenLink.objects.filter(user=user)
    hidden_lookup = set()
    for link in hidden:
        hidden_lookup.add(link.url)

    default = _get_default_links(affiliations)

    shown_defaults = []
    for link in default:
        if link['url'] not in hidden_lookup:
            shown_defaults.append({'url': link['url'],
                                   'label': link['label']
                                   })

    data['default_links'] = shown_defaults

    recents = []
    recent_links = VisitedLinkNew.recent_for_user(user)
    for link in recent_links:
        if link.url in existing_list_urls:
            continue
        added = link.url in custom_lookup
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
        with transaction.atomic():
            return CustomLink.objects.create(user=get_user_model(request),
                                             url=url,
                                             label=link_label)
    except IntegrityError:
        try:
            return get_custom_link_by_url(request, url)
        except Exception:
            log_err(logger,
                    "add_custom_link({}, {})".format(url, link_label),
                    traceback, request)
    return None


def delete_custom_link(request, link_id):
    try:
        link = get_custom_link_by_id(request, link_id)
        return link.delete()
    except Exception:
        log_err(logger, "delete_custom_link({})".format(link_id),
                traceback, request)
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
        log_err(logger,
                "edit_custom_link({}, {}, {})".format(
                    link_id, new_url, new_label), traceback, request)
    return None


def get_custom_link_by_id(request, link_id):
    return CustomLink.objects.get(pk=link_id, user=get_user_model(request))


def get_custom_link_by_url(request, url):
    return CustomLink.objects.get(user=get_user_model(request), url=url)


def add_hidden_link(request, url):
    try:
        with transaction.atomic():
            return HiddenLink.objects.create(user=get_user_model(request),
                                             url=url)
    except IntegrityError:
        try:
            return get_hidden_link_by_url(request, url)
        except Exception:
            log_err(logger, "add_hidden_link({})".format(url),
                    traceback, request)
    return None


def delete_hidden_link(request, link_id):
    try:
        link = get_hidden_link_by_id(request, link_id)
        return link.delete()
    except Exception:
        log_err(logger, "delete_hidden_link({})".format(link_id),
                traceback, request)
    return None


def get_hidden_link_by_id(request, link_id):
    return HiddenLink.objects.get(pk=link_id, user=get_user_model(request))


def get_hidden_link_by_url(request, url):
    return HiddenLink.objects.get(user=get_user_model(request), url=url)


def get_popular_link_by_id(link_id):
    return PopularLink.objects.get(pk=link_id)


def get_recent_link_by_id(request, link_id):
    return VisitedLinkNew.objects.get(pk=link_id,
                                      user=get_user_model(request))
