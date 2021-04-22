# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def teaching(request,
             year=None,
             quarter=None):
    context = get_context(year, quarter)
    return page(request, 'teaching.html', context=context)


@page_view
def teaching_section(request,
                     year,
                     quarter,
                     section):
    context = get_context(year, quarter, section)
    return page(request, 'teaching_section.html', context=context)


@page_view
def student_photo_list(request,
                       year,
                       quarter,
                       section):
    context = get_context(year, quarter, section)
    return page(request, 'teaching/photo_list.html', context=context)


def get_context(year, quarter, section=None):
    context = {}
    if year and quarter:
        context = {
            "display_term": {"year": year,
                             "quarter": quarter},
            }
    if section:
        context["section"] = "{},{},{}".format(year, quarter, section)
    return context
