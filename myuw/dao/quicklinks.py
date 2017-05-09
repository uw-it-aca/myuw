from myuw.models import VisitedLink, PopularLink, CustomLink, HiddenLink
from myuw.dao import get_netid_of_current_user, get_user_model
from myuw.dao.affiliation_data import get_data_for_affiliations
import csv
import os


RECENT_LINKS_DISPLAY_LIMIT = 5
CACHED_LABEL_DATA = {}


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
