from myuw.models import VisitedLink, PopularLink, CustomLink, HiddenLink
from myuw.dao import get_netid_of_current_user, get_user_model
import csv
import os


RECENT_LINKS_DISPLAY_LIMIT = 5


def get_quicklink_data():
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

    # TODO - consider affiliation filtering here
    popular_links = PopularLink.objects.all()
    for link in popular_links:
        added = link.url in custom_lookup
        existing_list_urls.add(link.url)
        popular.append({'added': added,
                        'url': link.url,
                        'label': link.label,
                        'id': link.pk})

    data['popular_links'] = popular

    # TODO - same here!
    hidden = HiddenLink.objects.filter(user=user)
    hidden_lookup = set()
    for link in hidden:
        hidden_lookup.add(link.url)

    default = _get_default_links()

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
                        'label': link.label,
                        'id': link.pk})

    data['recent_links'] = recents[:RECENT_LINKS_DISPLAY_LIMIT]

    return data


def _get_default_links():
    path = os.path.join(os.path.dirname(__file__),
                        '..', 'data', 'quicklinks.csv')

    defaults = []
    with open(path, 'rbU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # Skip header
        next(reader)
        for row in reader:
            defaults.append({'url': row[0], 'label': row[1]})

    return defaults
