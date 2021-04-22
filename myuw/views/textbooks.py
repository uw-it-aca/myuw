# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def textbooks(request, term=None, textbook=None):

    context = {
        'term': term,
        'textbook': textbook
    }

    return page(request, 'textbooks.html', context=context)
