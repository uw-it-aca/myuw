from myuw.dao.class_website import get_page_title_from_url
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views.error import data_not_found
from myuw.models import PopularLink, VisitedLink, CustomLink, HiddenLink
from myuw.dao import get_user_model, get_netid_of_current_user
from myuw.dao.quicklinks import get_quicklink_data
from myuw.dao.class_website import get_page_title_from_url
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
            label = get_page_title_from_url(url)
            link = True
            add_custom = True

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
        return HttpResponse(json.dumps(get_quicklink_data()))
