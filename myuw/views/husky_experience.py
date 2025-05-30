# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def husky_experience(request):
    return page(request, 'husky_experience.html')
