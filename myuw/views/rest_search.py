# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import re
from rc_django.views.rest_proxy import RestSearchView

logger = logging.getLogger(__name__)


class MyUWRestSearchView(RestSearchView):

    def get_proxy_url(self, request, service, url):
        """
        Convert form data to actual API urls.
        """
        params = None
        logger.debug(
            "Enter MyUWRestProxyView service: {}, url: {}, GET: {}".format(
                service, url, request.POST))

        if service == "book":
            url = "uw/json_utf8_202007.ubs"
            url = "{}?quarter={}&sln1={}&returnlink=t".format(
                "uw/json_utf8_202007.ubs",
                request.POST["quarter"],
                request.POST["sln1"])
        elif service == "grad":
            params = self.format_params(request)
        elif service == "hfs":
            url = "myuw/v1/{}".format(request.POST["uwnetid"])
        elif re.match(r'^iasystem', service):
            if url.endswith('/evaluation'):
                index = url.find('/')
                service = 'iasystem_' + url[:index]
                index += 1
                url = url[index:]
                params = self.format_params(request)
        elif service == "myplan":
            url = "student/api/plan/v1/{},{},1,{}".format(
                request.POST["year"],
                request.POST["quarter"],
                request.POST["uwregid"])
        elif service == "sws":
            if "advisers" == url:
                url = "student/v5/person/{}/advisers.json".format(
                    request.POST["uwregid"])
            elif "notices" == url:
                url = "student/v5/notice/{}.json".format(
                    request.POST["uwregid"])
        elif service == "uwnetid":
            if "password" == url:
                url = "nws/v1/uwnetid/{}/password".format(
                    request.POST["uwnetid"])
            elif "subscription" == url:
                url = "nws/v1/uwnetid/{}/subscription/60,64,105".format(
                    request.POST["uwnetid"])
        else:
            url, params = super().get_proxy_url(request, service, url)

        logger.debug(
            "Exit MyUWRestProxyView url: {}".format(url))
        return url, params
