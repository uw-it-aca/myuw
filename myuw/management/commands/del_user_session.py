# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from myuw.util.sessions import delete_sessions, SCOPE_IDTOKEN


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('netid', type=str, help="param1: uwnetid")
        parser.add_argument('scope', type=str, help="param2: {}|all".format(
            SCOPE_IDTOKEN))

    def handle(self, *args, **options):
        delete_sessions(options['netid'], options['scope'])
