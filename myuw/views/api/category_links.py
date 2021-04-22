# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import re
from myuw.dao.category_links import get_links_for_category
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_data_not_found_response
from myuw.logger.logresp import log_api_call
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found

logger = logging.getLogger(__name__)


class CategoryLinks(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/categorylinks/.
    """

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with links for the given category
        """
        category_id = kwargs.get('category_id')
        timer = Timer()
        links = get_links_for_category(category_id, request)
        if not links:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        link_data = self._group_links_by_subcategory(links)
        category_name = links[0].category_name

        log_api_call(timer, request,
                     "Get CategoryLinks for {}".format(category_name))
        return self.json_response({"link_data": link_data,
                                   "category_name": category_name})

    def _group_links_by_subcategory(self, links):
        ordered_subcategories = []
        subcategory_data = {}
        link_output = []
        for link in links:
            sub_cat = link.sub_category
            sub_cat_slug = re.sub(r'\W+', '', sub_cat).lower()

            if sub_cat in subcategory_data:
                subcategory_data[sub_cat]['links'].append(link.json_data())
            else:
                ordered_subcategories.append(sub_cat)
                subcategory_data[sub_cat] = {}
                subcategory_data[sub_cat]['links'] = [link.json_data()]
                subcategory_data[sub_cat]['subcategory'] = sub_cat
                subcategory_data[sub_cat]['subcat_slug'] = sub_cat_slug

        for subcat_group in ordered_subcategories:
            data = sorted(subcategory_data[subcat_group]['links'],
                          key=lambda k: k['title']
                          )
            subcategory_data[subcat_group]['links'] = data
            link_output.append(subcategory_data[subcat_group])
        return link_output
