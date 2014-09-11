from django.db.models import Q
from myuw_mobile.models import CategoryLinks
from myuw_mobile.dao.affiliation import get_all_affiliations
import csv
import os


def _get_campus():
    campus = ""
    affiliations = get_all_affiliations()
    try:
        if affiliations["official_tacoma"]:
            campus = "tacoma"
        if affiliations["official_bothell"]:
            campus = "bothell"
        if affiliations["official_seattle"]:
            campus = "seattle"
    except KeyError:
        try:
            if affiliations["tacoma"]:
                campus = "tacoma"
            if affiliations["bothell"]:
                campus = "bothell"
            if affiliations["seattle"]:
                campus = "seattle"
        except KeyError:
            campus = ""
            pass
    return campus




def get_links_for_category(search_category_id):
    campus = _get_campus()

    links = []
    path = os.path.join(
        os.path.dirname( __file__ ),
        '..', 'data', 'category_links_import.csv')
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in reader:
            category = row[0]
            category_id = _get_category_id(category)
            subcategory = row[1]
            central_url = row[2]
            central_title = row[3]
            seattle_url = row[4]
            seattle_title = row[5]
            bothell_url = row[6]
            bothell_title = row[7]
            tacoma_url = row[8]
            tacoma_title = row[9]
            if (category_id != search_category_id):
                continue

            if len(central_url) > 0:
                link = CategoryLinks(
                    url=central_url,
                    title=central_title,
                    category_name=category,
                    sub_category=subcategory
                )
                if len(central_title) == 0:
                    link.title = link.url
                links.append(link)

            if len(seattle_url) > 0 and campus == "seattle":
                print 'adding campus'
                link = CategoryLinks(
                    url=seattle_url,
                    title=seattle_title,
                    category_name=category,
                    sub_category=subcategory,
                    campus="seattle"
                )
                if len(seattle_title) == 0:
                    link.title = link.url
                link.set_category_id(category)
                links.append(link)
            if len(bothell_url) > 0 and campus == "bothell":
                link = CategoryLinks(
                    url=bothell_url,
                    title=bothell_title,
                    category_name=category,
                    sub_category=subcategory,
                    campus="bothell"
                )
                if len(bothell_title) == 0:
                    link.title = link.url
                link.set_category_id(category)
                links.append(link)
            if len(tacoma_url) > 0 and campus == "tacoma":
                link = CategoryLinks(
                    url=tacoma_url,
                    title=tacoma_title,
                    category_name=category,
                    sub_category=subcategory,
                    campus="tacoma"
                )
                if len(tacoma_title) == 0:
                    link.title = link.url
                link.set_category_id(category)
                links.append(link)
    return links


def _get_category_id(category_name):
    category_id = category_name.lower()
    category_id = "".join(c for c in category_id if c.isalpha())
    return category_id