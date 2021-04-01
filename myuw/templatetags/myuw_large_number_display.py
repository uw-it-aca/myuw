# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.template import Library


register = Library()


@register.simple_tag()
def large_number(value):
    if value < 1000:
        return value

    for label in ['K', 'M', 'B']:
        value //= 1000
        if value < 1000:
            return "{}{}".format(value, label)

    return "{}{}".format(value, label)
