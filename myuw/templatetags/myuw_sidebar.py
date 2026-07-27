# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.template import Library
from django.urls import resolve

register = Library()


@register.simple_tag(takes_context=True)
def add_sidebar_context(context):
    request = context.get('request')
    if not request:
        return ''

    current_url = resolve(request.path_info).url_name

    context[f"is_{current_url}"] = True

    for f in getattr(settings, "MYUW_ENABLED_FEATURES", []):
        context[f"{f.lower()}_enabled"] = True

    return ''
