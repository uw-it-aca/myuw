#!/usr/bin/python
"""
Test all the links in the CSV for non-200 status codes (after redirects).
"""

import sys
from django.core.management.base import BaseCommand, CommandError
from myuw.dao import has_newmyuw_preference, has_legacy_preference


class Command(BaseCommand):

    help = "Find the Migration Preference for the given user"

    def add_arguments(self, parser):
        parser.add_argument('netid')

    def handle(self, *args, **options):
        username = options['netid']
        if has_legacy_preference(username):
            print "%s prefers the legacy MyUW" % username
            return
        if has_newmyuw_preference(username):
            print "%s prefer the new MyUW" % username
            return
        print "%s doesn't have a preference" % username
