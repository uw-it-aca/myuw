from myuw.dao.class_website import get_page_title_from_url
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views.error import data_not_found, invalid_input_data
from myuw.models import PopularLink, VisitedLink, CustomLink, HiddenLink
from myuw.dao import get_user_model, get_netid_of_current_user
from myuw.dao.quicklinks import get_quicklink_data
from myuw.dao.class_website import get_page_title_from_url
from myuw.dao.affiliation import get_all_affiliations
from restclients.exceptions import DataFailureException
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.db import transaction, IntegrityError
import json
import re


class ManageLinks(RESTDispatch):
    @method_decorator(csrf_protect)
    def POST(self, request):
        try:
            data = json.loads(request.body)
        except ValueError:
            return data_not_found()

        if "label" in data:
            data["label"] = data["label"].strip()
            if "" == data["label"]:
                return invalid_input_data()
        link = False
        url = None
        label = None
        add_custom = False
        if "type" not in data:
            return data_not_found()

        user = get_user_model()
        if "popular" == data["type"]:
            try:
                link = PopularLink.objects.get(pk=data['id'])
                url = link.url
                label = link.label
                link = True
                add_custom = True
            except PopularLink.DoesNotExist:
                return data_not_found()

        elif "recent" == data["type"]:
            try:
                username = get_netid_of_current_user()
                link = VisitedLink.objects.get(pk=data['id'],
                                               username=username)
                url = link.url
                label = link.label
                link = True
                add_custom = True
            except VisitedLink.DoesNotExist:
                return data_not_found()

        elif "custom" == data["type"]:
            url = data["url"]
            if not re.match('^https?://', url):
                url = "http://%s" % url
            try:
                label = get_page_title_from_url(url)
            except DataFailureException:
                return data_not_found()
            link = True
            add_custom = True

        elif "custom-edit" == data["type"]:
            try:
                link = CustomLink.objects.get(pk=data['id'],
                                              user=user)
            except CustomLink.DoesNotExist:
                return data_not_found()

            url = data["url"]
            if not re.match('^https?://', url):
                url = "http://%s" % url
            label = data["label"]

            link.url = url
            link.label = label

            link.save()

        elif "remove" == data["type"]:
            link_id = data['id']
            try:
                link = CustomLink.objects.get(user=user, pk=link_id)
                link.delete()
            except CustomLink.DoesNotExist:
                return data_not_found()

        elif "hide" == data["type"]:
            try:
                with transaction.atomic():
                    HiddenLink.objects.create(user=user, url=data["id"])
            except IntegrityError as ex:
                pass
            link = True

        if not link:
            return data_not_found()

        if add_custom:
            try:
                with transaction.atomic():
                    CustomLink.objects.create(user=user,
                                              url=url,
                                              label=label)
            except IntegrityError as ex:
                pass
        affiliations = get_all_affiliations(request)
        return HttpResponse(json.dumps(get_quicklink_data(affiliations)))
