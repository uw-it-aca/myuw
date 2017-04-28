from myuw.models import VisitedLink, PopularLink, CustomLink
from myuw.dao import get_netid_of_current_user, get_user_model


def get_quicklink_data():
    data = {}

    username = get_netid_of_current_user()

    custom = []
    custom_lookup = set()
    user = get_user_model()
    custom_links = CustomLink.objects.filter(user=user).order_by('pk')
    for link in custom_links:
        custom_lookup.add(link.url)
        custom.append({'url': link.url, 'label': link.label, 'id': link.pk})

    data['custom_links'] = custom

    recents = []
    recent_links = VisitedLink.recent_for_user(username)
    for link in recent_links:
        added = link.url in custom_lookup
        recents.append({'added': added,
                        'url': link.url,
                        'label': link.label,
                        'id': link.pk})

    data['recent_links'] = recents

    popular = []

    # TODO - consider affiliation filtering here
    popular_links = PopularLink.objects.all()
    for link in popular_links:
        added = link.url in custom_lookup
        popular.append({'added': added,
                        'url': link.url,
                        'label': link.label,
                        'id': link.pk})

    data['popular_links'] = popular

    return data
