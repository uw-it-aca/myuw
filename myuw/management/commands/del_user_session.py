# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand

from myuw.util.sessions import SCOPE_IDTOKEN, delete_sessions


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('netid', type=str, help="param1: uwnetid")
        parser.add_argument('scope', type=str, help=f"param2: {SCOPE_IDTOKEN}|all")

    def handle(self, *args, **options):
        delete_sessions(options['netid'], options['scope'])
