# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.dao.term import get_current_quarter
from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def teaching(request,
             year=None,
             quarter=None):
    if year is None and quarter is None:
        # MUWM-5363
        term = get_current_quarter(request)
        context = get_context(term.year, term.quarter)
    else:
        context = get_context(year, quarter)
    return page(request, 'teaching.html', context=context)


@page_view
def teaching_section(request,
                     year,
                     quarter,
                     section):
    context = get_context(year, quarter, section)
    return page(request, 'teaching.html', context=context)


@page_view
def student_photo_list(request,
                       year,
                       quarter,
                       section):
    context = get_context(year, quarter, section)
    return page(request, 'teaching_classlist.html', context=context)


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
