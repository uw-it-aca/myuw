import csv
import os
from django.db.models import Q
from myuw.models.res_category_link import ResCategoryLink
from myuw.dao.affiliation import get_all_affiliations, get_base_campus


class MyuwLink:
    """
    Read the resource links from a file and store them
    in an array of Link objects.
    """

    _singleton = None

    def __init__(self):
        self.links = []
        path = os.path.join(
            os.path.dirname(__file__),
            '..', 'data', self.csv_filename)

        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                category = row[0]
                if category == 'Category':
                    continue
                category_id = _get_category_id(category)
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


class Explore_Links(MyuwLink):
    """
    Read the explore links from a file and store them
    in an array of ResCategoryLink objects.
    """

    _singleton = None
    csv_filename = 'explore_link_import.csv'

    def get_grouped_links(self):
        if self.links is None:
            self.links = self.get_all_links()
        grouped_links = {}
        for link in self.links:
            category = grouped_links.setdefault(link.category_name, [])
            if link.sub_category not in category:
                category.append(link.sub_category)
        link_list = [{k: v} for k, v in grouped_links.items()]
        return link_list


def _get_category_id(category_name):
    category_id = category_name.lower()
    category_id = "".join(c for c in category_id if c.isalpha())
    return category_id


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

        if link.all_affiliation() and link.campus_matched(campus):
            selected_links.append(link)
            continue

        if link.campus_matched(campus) and\
                affiliations["grad"] and link.for_grad():
            selected_links.append(link)
            continue

        if link.campus_matched(campus) and\
                affiliations["undergrad"] and link.for_undergrad():
            selected_links.append(link)
            continue

        if link.campus_matched(campus) and\
                affiliations["fyp"] and link.for_fyp():
            selected_links.append(link)
            continue

        if link.campus_matched(campus) and\
                affiliations["pce"] and link.for_pce():
            selected_links.append(link)
            continue

    return selected_links
