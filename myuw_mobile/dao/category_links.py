from myuw_mobile.models import CategoryLinks


def get_links_for_category(category):
    links = CategoryLinks.objects.filter(category=category)

    return links
