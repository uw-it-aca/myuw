import json
import logging
import re
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from restclients_core.exceptions import DataFailureException
from myuw.dao.class_website import get_page_title_from_url
from myuw.dao.quicklinks import get_quicklink_data, get_link_label,\
    add_custom_link, delete_custom_link, edit_custom_link,\
    add_hidden_link, delete_hidden_link, get_popular_link_by_id,\
    get_recent_link_by_id
from myuw.dao.class_website import get_page_title_from_url
from myuw.dao.affiliation import get_all_affiliations
from myuw.models import PopularLink, VisitedLink, CustomLink, HiddenLink
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views.error import data_not_found, invalid_input_data


logger = logging.getLogger(__name__)


class ManageLinks(RESTDispatch):
    @method_decorator(csrf_protect)
    def POST(self, request):
        try:
            data = json.loads(request.body)
        except ValueError:
            return data_not_found()

        def clean(field):
            if field not in data:
                return True
            data[field] = data[field].strip()
            if "" == data[field]:
                return False
            return True

        for field in ("label", "url"):
            if not clean(field):
                return invalid_input_data()

        link = None
        if "type" not in data:
            return data_not_found()

        if "popular" == data["type"]:
            link_id = get_link_id(data)
            if link_id:
                try:
                    link = get_popular_link_by_id(link_id)
                except PopularLink.DoesNotExist:
                    return data_not_found()
                link = add_custom_link(link.url, link.label)

        elif "recent" == data["type"]:
            link_id = get_link_id(data)
            if link_id:
                try:
                    link = get_recent_link_by_id(link_id)
                except VisitedLink.DoesNotExist:
                    return data_not_found()
                link = add_custom_link(link.url, link.label)

        elif "custom" == data["type"]:
            url, label = get_link_data(data, get_id=False)
            if url and label:
                link = add_custom_link(url, label)
            else:
                return data_not_found()

        elif "custom-edit" == data["type"]:
            link_id, new_url, new_label = get_link_data(data)
            if link_id and new_url:
                link = edit_custom_link(link_id, new_url, new_label)
            else:
                return data_not_found()

        elif "remove" == data["type"]:
            link_id = get_link_id(data)
            if link_id:
                link = delete_custom_link(link_id)
            else:
                return data_not_found()

        elif "hide" == data["type"]:
            url = get_link_url(data)
            if url:
                link = add_hidden_link(url)
            else:
                return data_not_found()

        if not link:
            return data_not_found()

        affiliations = get_all_affiliations(request)
        return HttpResponse(json.dumps(get_quicklink_data(affiliations)))


def get_link_id(data):
    return data.get('id')


def get_link_url(data):
    if 'url' in data and len(data["url"]):
        return data["url"]
    return None


def get_link_data(data, get_id=True):
    url = get_link_url(data)

    if "label" in data and len(data["label"]):
        label = data["label"]
    else:
        if not re.match('^[a-z]+://', url):
            full_url = "http://%s" % url
        else:
            full_url = url

        try:
            label = get_page_title_from_url(full_url)
        except DataFailureException:
            label = url

    if get_id:
        link_id = get_link_id(data)
        return link_id, url, label
    else:
        return url, label
