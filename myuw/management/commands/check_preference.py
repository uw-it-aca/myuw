#!/usr/bin/python
"""
Test all the links in the CSV for non-200 status codes (after redirects).
"""

import sys
from django.core.management.base import BaseCommand, CommandError
from myuw.models import UserMigrationPreference


class Command(BaseCommand):
    args = "<user netid>"
    help = "Find the Migration Preference for the given user"

    def handle(self, *args, **kwargs):
        if len(args) < 1:
            raise CommandError("Invalid argument %s" % args)
        username = args[0]
        pref = False
        try:
            saved = UserMigrationPreference.objects.get(username=username)
            if saved.use_legacy_site:
                pref = True
        except UserMigrationPreference.DoesNotExist:
            pass
        if pref:
            print "%s prefers the legacy MyUW" % username
        else:
            print "%s doesn't prefer the legacy MyUW" % username
