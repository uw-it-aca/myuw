import logging
import json
import re
from django.db import transaction, IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from restclients_core.exceptions import DataFailureException
from myuw.dao import is_action_disabled
from myuw.dao.quicklinks import (
    get_quicklink_data, get_link_label, add_custom_link, delete_custom_link,
    edit_custom_link, add_hidden_link, delete_hidden_link,
    get_popular_link_by_id, get_recent_link_by_id)
from myuw.models import PopularLink, VisitedLinkNew, CustomLink, HiddenLink
from myuw.logger.logresp import log_api_call
from myuw.logger.timer import Timer
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, invalid_input_data,\
    disabled_action_error

logger = logging.getLogger(__name__)


class ManageLinks(ProtectedAPI):

    def get(self, request, *args, **kwargs):
        timer = Timer()
        try:
            data = get_quicklink_data(request)
            log_api_call(timer, request, "Get Quicklinks")
            return self.json_response(get_quicklink_data(request))
        except Exception as ex:
            return handle_exception(logger, timer, traceback)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        if is_action_disabled():
            return disabled_action_error()

        timer = Timer()
        try:
            data = json.loads(request.body)
        except ValueError:
            return data_not_found()

        def clean(field):
            if field not in data:
                return True
            pre = data[field]
            data[field] = data[field].strip()
            if "" == data[field] and "" != pre:
                return False
            return True

        if not clean("url"):
            return invalid_input_data()

        if 'label' in data:
            data['label'] = data['label'].strip()

        link = None
        if "type" not in data:
            return data_not_found()

        if "popular" == data["type"]:
            link_id = get_link_id(data)
            if link_id:
                try:
                    plink = get_popular_link_by_id(link_id)
                except PopularLink.DoesNotExist:
                    return data_not_found()
                link = add_custom_link(request, plink.url, plink.label)
                log_api_call(timer, request,
                             "Popular==>Custom link ({})".format(plink.url))

        elif "recent" == data["type"]:
            link_id = get_link_id(data)
            if link_id:
                try:
                    vlink = get_recent_link_by_id(request, link_id)
                except VisitedLinkNew.DoesNotExist:
                    return data_not_found()
                link = add_custom_link(request, vlink.url, vlink.label)
                log_api_call(timer, request,
                             "Recent==>Custom link ({})".format(vlink.url))

        elif "custom" == data["type"]:
            # add a custom link
            url, label = get_link_data(data, get_id=False)
            if url and label:
                link = add_custom_link(request, url, label)
                log_api_call(timer, request,
                             "Add Custom link ({})".format(url))
            else:
                return data_not_found()

        elif "custom-edit" == data["type"]:
            link_id, new_url, new_label = get_link_data(data)
            if link_id and new_url:
                link = edit_custom_link(request, link_id, new_url, new_label)
                log_api_call(timer, request,
                             "Edit Custom link ({})".format(new_url))
            else:
                return data_not_found()

        elif "remove" == data["type"]:
            # remove a custom link
            link_id = get_link_id(data)
            if link_id:
                link = delete_custom_link(request, link_id)
            else:
                return data_not_found()

        elif "hide" == data["type"]:
            # hide a default link
            url = get_link_id(data)
            if url:
                link = add_hidden_link(request, url)
                log_api_call(timer, request,
                             "Hide Default link ({})".format(url))
            else:
                return data_not_found()

        if not link:
            return data_not_found()

        return self.json_response(get_quicklink_data(request))


def get_link_id(data):
    return data.get('id')


def get_link_url(data):
    """
    return full URL
    """
    url = data.get('url')
    if url:
        if not re.match('^[a-z]+://', url):
            return "http://{}".format(url)
        return url
    return None


def get_link_label(data):
    return data.get('label')


def get_link_data(data, get_id=True):
    url = get_link_url(data)

    label = get_link_label(data)
    if not label:
        label = url

    if get_id:
        link_id = get_link_id(data)
        return link_id, url, label
    else:
        return url, label
