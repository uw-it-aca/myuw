#!/usr/bin/python
"""
Test all the links in the CSV for non-200 status codes (after redirects).
"""

import sys
from django.core.management.base import BaseCommand, CommandError
from myuw.dao import set_preference_to_new_myuw, set_preference_to_old_myuw


class Command(BaseCommand):

    help = "Change the preference for the given user"

    def add_arguments(self, parser):
        parser.add_argument('netid')
        parser.add_argument('pref', choices=['old', 'new'])

    def handle(self, *args, **options):
        netid = options['netid']
        pref = options['pref']

        if pref == 'old':
            set_preference_to_old_myuw(netid)
            print "%s has been switched back to the legacy MyUW" % netid
        elif pref == 'new':
            set_preference_to_new_myuw(netid)
            print "%s has been switched to the new MyUW" % netid
        else:
            pass
