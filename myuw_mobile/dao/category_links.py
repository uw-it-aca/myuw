from django.db.models import Q
from myuw_mobile.models import CategoryLinks
from myuw_mobile.dao.affiliation import get_all_affiliations


def get_links_for_category(category_id):
    _get_campus()
    links = CategoryLinks.objects.filter(Q(category_id=category_id),
                                         Q(campus=_get_campus()) | Q(campus=None))
    return links


def _get_campus():
    campus = ""
    affiliations = get_all_affiliations()

    if affiliations["tacoma"]:
        campus = "tacoma"
    if affiliations["bothell"]:
        campus = "bothell"
    if affiliations["seattle"]:
        campus = "seattle"
    return campus