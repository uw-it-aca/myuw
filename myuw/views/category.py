# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def category(request, category=None, topic=None):
    context = {
        'category': category,
        'topic': topic
    }
    return page(request, 'category.html', context=context)
