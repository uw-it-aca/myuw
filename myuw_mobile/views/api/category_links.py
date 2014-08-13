from django.http import HttpResponse
import json
import logging
import re
from myuw_mobile.dao.category_links import get_links_for_category
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found


class CategoryLinks(RESTDispatch):
    """
    Performs actions on resource at /api/v1/categorylinks/.
    """

    def GET(self, request, category_id):
        """
        GET returns 200 with links for the given category
        """
        timer = Timer()
        logger = logging.getLogger('views.api.CategoryLinks.GET')
        links = get_links_for_category(category_id)
        if not links:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        link_data = self._group_links_by_subcategory(links)
        category_name = links[0].category_name

        log_success_response(logger, timer)
        return HttpResponse(json.dumps({"link_data": link_data,
                                        "category_name": category_name}))


    def _group_links_by_subcategory(self, links):
        subcategory_data = {}
        link_output = []
        for link in links:
            sub_cat = link.sub_category
            sub_cat_slug = re.sub(r'\W+', '', sub_cat).lower()
            
            if sub_cat in subcategory_data:
                subcategory_data[sub_cat]['links'].append(link.json_data())
            else:
                subcategory_data[sub_cat] = {}
                subcategory_data[sub_cat]['links'] = [link.json_data()]
                subcategory_data[sub_cat]['subcategory'] = sub_cat
                subcategory_data[sub_cat]['subcat_slug'] = sub_cat_slug

        for subcat_group in subcategory_data:
            subcategory_data[subcat_group]['links'] = sorted(subcategory_data[subcat_group]['links'],
                                                          key=lambda k: k['title'])
            link_output.append(subcategory_data[subcat_group])
        return link_output
