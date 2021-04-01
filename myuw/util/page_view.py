# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


def page_view(func):
    @login_required
    @cache_control(max_age=0, no_cache=True,
                   no_store=True, must_revalidate=True)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
