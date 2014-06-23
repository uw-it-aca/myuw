from myuw_mobile.models import CategoryLinks


def get_links_for_category(category_id):
    links = CategoryLinks.objects.filter(category_id=category_id)

    return links
