# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django import template
from django.template import Library
from myuw.dao.admin import is_admin, can_override


register = Library()


@register.simple_tag(takes_context=True)
def add_admin_checks(context):
    context['is_myuw_admin'] = is_admin()
    context['is_overrider'] = can_override()  # including admin
    return ''
