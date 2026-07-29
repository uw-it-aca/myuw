# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import hashlib

from django import template

register = template.Library()


@register.simple_tag
def hash_netid(netid):
    if netid is not None:
        return hashlib.md5(netid.encode('utf-8')).hexdigest()
    return ''
