import csv
import os
from copy import deepcopy
from django.db.models import Q
from myuw.models import ResourceCategoryPin
from myuw.models.res_category_link import ResCategoryLink
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.user import get_user_model
from myuw.dao.exceptions import InvalidResourceCategory


class MyuwLink:
    """
    Read the resource links from a file and store them
    in an array of Link objects.
    """

    _singleton = None

    def __init__(self, csv_filename=None):
        if csv_filename:
            self.csv_filename = csv_filename
        self.links = []
        path = os.path.join(os.path.dirname(__file__),
                            '..', 'data', self.csv_filename)

        with open(path, 'r', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                # print(', '.join(row))
                category = row[0]
                if category == 'Category':
                    continue
                subcategory = row[1]
                affiliation = row[2]
                central_url = row[3]
                central_title = row[4]
                seattle_url = row[5]
                seattle_title = row[6]
                bothell_url = row[7]
                bothell_title = row[8]
                tacoma_url = row[9]
                tacoma_title = row[10]

                new_tab = False
                if row[11] == "yes":
                    new_tab = True

                if len(central_url) > 0:
                    link = ResCategoryLink(
                        url=central_url,
                        title=central_title,
                        affiliation=affiliation,
                        category_name=category,
                        sub_category=subcategory,
                        new_tab=new_tab
                        )
                    link.set_category_id(category)
                    link.set_subcategory_id(subcategory)
                    self.links.append(link)

                if len(seattle_url) > 0:
                    link = ResCategoryLink(
                        url=seattle_url,
                        title=seattle_title,
                        affiliation=affiliation,
                        campus=ResCategoryLink.SEATTLE,
                        category_name=category,
                        sub_category=subcategory,
                        new_tab=new_tab
                        )
                    link.set_category_id(category)
                    link.set_subcategory_id(subcategory)
                    self.links.append(link)

                if len(bothell_url) > 0:
                    link = ResCategoryLink(
                        url=bothell_url,
                        title=bothell_title,
                        affiliation=affiliation,
                        campus=ResCategoryLink.BOTHELL,
                        category_name=category,
                        sub_category=subcategory,
                        new_tab=new_tab
                        )
                    link.set_category_id(category)
                    link.set_subcategory_id(subcategory)
                    self.links.append(link)

                if len(tacoma_url) > 0:
                    link = ResCategoryLink(
                        url=tacoma_url,
                        title=tacoma_title,
                        affiliation=affiliation,
                        campus=ResCategoryLink.TACOMA,
                        category_name=category,
                        sub_category=subcategory,
                        new_tab=new_tab
                        )
                    link.set_category_id(category)
                    link.set_subcategory_id(subcategory)
                    self.links.append(link)

    @classmethod
    def get_all_links(cls):
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton.links


class Res_Links(MyuwLink):
    """
    Read the resource links from a file and store them
    in an array of ResCategoryLink objects.
    """

    _singleton = None
    csv_filename = 'category_links_import.csv'


class Resource_Links(MyuwLink):
    """
    Read the explore links from a file and store them
    in an array of ResCategoryLink objects.
    """

    _singleton = None
    csv_filename = 'resource_link_import.csv'

    def get_all_grouped_links(self, request):
        category_list = []
        user = get_user_model(request)
        pinned = ResourceCategoryPin.get_user_pinned_categories(user)
        grouped_links = self.get_grouped_links(request, pinned)

        for category in grouped_links:
            category_list.append(grouped_links[category])

        return category_list

    def get_pinned_links(self, request):
        category_list = []
        user = get_user_model(request)
        pinned = ResourceCategoryPin.get_user_pinned_categories(user)
        grouped_links = self.get_grouped_links(request, pinned)
        self._filter_pinned(grouped_links)

        for category in grouped_links:
            category_list.append(grouped_links[category])

        return category_list

    def _filter_pinned(self, links):
        # python 3 RuntimeError: dictionary changed size during iteration
        # Add deepcopy. Fang 2018/10/11

        # remove unpinned subcats
        for category in deepcopy(links):
            for subcat in deepcopy(links[category]['subcategories']).keys():
                if not links[category]['subcategories'][subcat]['is_pinned']:
                    del links[category]['subcategories'][subcat]

        # remove cats w/o subcat
        for category in deepcopy(links).keys():
            subcat = links[category]['subcategories']
            if len(subcat) == 0:
                del links[category]

        return links

    def get_grouped_links(self, request, pinned_list=[]):
        if self.links is None:
            self.links = self.get_all_links()

        grouped_links = {}
        affiliations = get_all_affiliations(request)
        campus = get_base_campus(affiliations)

        for link in self.links:
            link = _get_link_by_affiliation(link, campus, affiliations)
            if link:
                if link.category_id not in grouped_links:
                    grouped_links[link.category_id] = \
                        {'category_name': link.category_name,
                         'category_id': link.category_id,
                         'subcategories': {}}
                subcats = grouped_links[link.category_id]['subcategories']
                if link.sub_category not in subcats:
                    subcat_id = link.category_id.lower() + \
                                link.subcategory_id.lower()
                    is_pinned = subcat_id in pinned_list
                    try:
                        order = pinned_list.index(subcat_id)
                    except ValueError:
                        order = None
                    subcats[link.sub_category] = \
                        {'subcat_name': link.sub_category,
                         'subcat_id': subcat_id,
                         'is_pinned': is_pinned,
                         'order': order,
                         'links': []}

                subcats[link.sub_category]['links'].append(
                    {'title': link.title,
                     'url': link.url})
        return grouped_links

    def category_exists(self, category_id):
        if self.links is None:
            self.links = self.get_all_links()
        for link in self.links:
            link_cat_id = link.category_id + link.subcategory_id
            if category_id == link_cat_id.lower():
                return True
        return False


def get_links_for_category(search_category_id, request):
    affiliations = get_all_affiliations(request)
    return _get_links_by_category_and_campus(search_category_id,
                                             get_base_campus(affiliations),
                                             affiliations)


def _get_links_by_category_and_campus(search_category_id,
                                      campus,
                                      affiliations):
    selected_links = []
    all_links = Res_Links.get_all_links()

    for link in all_links:
        if not link.category_id_matched(search_category_id):
            continue
        customized_link = _get_link_by_affiliation(link, campus, affiliations)
        if customized_link:
            selected_links.append(customized_link)

    return selected_links


def _get_link_by_affiliation(link, campus, affiliations):
    if link.all_affiliation() and link.campus_matched(campus):
        return link

    if link.campus_matched(campus) and \
            affiliations["grad"] and link.for_grad():
        return link

    if link.campus_matched(campus) and \
            affiliations["undergrad"] and link.for_undergrad():
        return link

    """
    MUWM-4831
    if link.campus_matched(campus) and \
            affiliations["fyp"] and link.for_fyp():
        return link
    """

    if link.campus_matched(campus) and \
            affiliations["pce"] and link.for_pce():
        return link


def pin_category(request, category_id):
    user = get_user_model(request)
    rs = Resource_Links()
    if rs.category_exists(category_id):
        rs_pin = ResourceCategoryPin.objects.\
            get_or_create(user=user, resource_category_id=category_id)
    else:
        raise InvalidResourceCategory(category_id)


def delete_categor_pin(request, category_id):
    user = get_user_model(request)
    pinned = ResourceCategoryPin.objects.\
        get(user=user, resource_category_id=category_id)
    if pinned:
        pinned.delete()


def get_base_campus(affiliations):
    """
    Return one currently enrolled campus.
    If not exist, return one affiliated campus.
    """
    is_stud = affiliations["student"]
    if (is_stud and affiliations.get("seattle") is True or
            affiliations.get("official_seattle") is True):
        return "seattle"
    if (is_stud and affiliations.get("bothell") is True or
            affiliations.get("official_bothell") is True):
        return "bothell"
    if (is_stud and affiliations.get("tacoma") is True or
            affiliations.get("official_tacoma") is True):
        return "tacoma"
    return ""
