# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django import template
import hashlib

register = template.Library()


@register.simple_tag
def hash_netid(netid):
    if netid is not None:
        return hashlib.md5(netid.encode('utf-8')).hexdigest()
    return ''
