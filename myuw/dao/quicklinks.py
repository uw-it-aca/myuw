import csv
import logging
import os
from django.db import transaction, IntegrityError
from myuw.models import VisitedLink, PopularLink, CustomLink, HiddenLink
from myuw.dao import get_netid_of_current_user, get_user_model
from myuw.dao.affiliation_data import get_data_for_affiliations


RECENT_LINKS_DISPLAY_LIMIT = 5
CACHED_LABEL_DATA = {}
logger = logging.getLogger(__name__)


def get_quicklink_data(affiliations):
    data = {}

    username = get_netid_of_current_user()

    # For excluding from the recent list
    existing_list_urls = set()
    custom = []
    custom_lookup = set()
    user = get_user_model()
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
    recent_links = VisitedLink.recent_for_user(username)
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
        with open(path, 'rbU') as csvfile:
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


def add_hidden_link(url):
    try:
        with transaction.atomic():
            return HiddenLink.objects.create(user=get_user_model(),
                                             url=url)
    except IntegrityError as ex:
        logger.error("%s add_hidden_link(%s) ==> %s",
                     get_netid_of_current_user(), url, ex)
    return None


def delete_hidden_link(link_id):
    try:
        link = HiddenLink.objects.get(url_key=link_id,
                                      user=get_user_model())
        return link.delete()
    except HiddenLink.DoesNotExist as ex:
        logger.error("%s delete_hidden_link(%s) ==> %s",
                     get_netid_of_current_user(), link_id, ex)
    return None


def add_custom_link(url, link_label=None):
    try:
        with transaction.atomic():
            return CustomLink.objects.create(user=get_user_model(),
                                             url=url,
                                             label=link_label)
    except IntegrityError as ex:
        logger.error("%s add_custom_link(%s, %s) ==> %s",
                     get_netid_of_current_user(), url, link_label, ex)
    return None


def delete_custom_link(link_id):
    try:
        link = CustomLink.objects.get(user=get_user_model(),
                                      url_key=link_id)
        return link.delete()
    except CustomLink.DoesNotExist as ex:
        logger.error("%s delete_custom_link(%s) ==> %s",
                     get_netid_of_current_user(), link_id, ex)
    return None


def edit_custom_link(link_id, new_url, new_label=None):
    try:
        link = CustomLink.objects.get(url_key=link_id,
                                      user=get_user_model())
        link.url = new_url
        if new_label is not None and len(new_label):
            link.label = new_label
        link.save()
        return link
    except CustomLink.DoesNotExist as ex:
        logger.error("%s edit_custom_link(%s, %s, %s) ==> %s",
                     get_netid_of_current_user(), link_id,
                     new_url, new_label, ex)
    return None
