#!/usr/bin/python
"""
Test all the links in the CSV for non-200 status codes (after redirects).
"""

import sys
import urllib3

from django.core.management.base import BaseCommand, CommandError
from myuw.dao.messages import get_current_messages

# Disable SSL warnings
urllib3.disable_warnings()
# Need limit of 1, otherwise sdb gives us a 403
http = urllib3.PoolManager(1, timeout=8)
# Need to override UA for some links, e.g. LinkedIn


class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        from myuw.test import fdao_sws_override, fdao_pws_override,\
        get_request, get_request_with_user

        get_current_messages(get_request_with_user('javerage'))
