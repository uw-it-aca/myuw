# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def set_context(context, name, value):
    """
    Sets a variable for this template, and its parent template
    """
    context[name] = value
    current = context.pop()
    context[name] = value
    context.push(current)
    return ''
