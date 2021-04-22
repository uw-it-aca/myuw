# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.util.page_view import page_view
from myuw.views.page import page


@page_view
def index(request):
    return page(request, 'index.html', add_quicklink_context=True)
