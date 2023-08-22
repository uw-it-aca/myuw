# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from django.db import connections
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import UwAccount
from sis_provisioner.util.log import log_resp_time, Timer


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'action', choices=[
                'all', 'prep', 'dump', 'load', 'inspect', 'tidy'
            ]
        )

    def handle(self, *args, **options):
        self.fixture_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'mysql_data_fixture.json')

        self.action = options['action']

        if self.action == 'prep':
            self.prep()
        if self.action == 'dump':
            self.dump_mysql_data()
        if self.action == 'load':
            self.load_postgresdb()
        if self.action == 'inspect':
            self.inspect_postgresqldb()
        if self.action == 'tidy':
            self.cleanup()

        if self.action == 'all':
            self.prep()
            self.dump_mysql_data()
            self.load_postgresdb()
            self.inspect_postgresqldb()
            self.cleanup()

    def prep(self):
        logger.info("{} UwAccounts in mysql DB".format(
            len(UwAccount.objects.using('mysql').all())))
        # with connections['mysql'].cursor() as cursor:
        # cursor.execute("DELETE FROM django_session")

    def dump_mysql_data(self):
        timer = Timer()
        try:
            model_list = ['sis_provisioner.UwAccount']
            call_command(
                'dumpdata', *model_list, '--database=mysql',
                output=self.fixture_file)
        except CommandError as e:
            logger.error("Dump table from the MySQL DB: {}".format(e))
        log_resp_time(logger, "dump_mysql_data", timer)

    def load_postgresdb(self):
        timer = Timer()
        try:
            call_command('loaddata', self.fixture_file)
        except CommandError as e:
            logger.error("Load data into Postgres DB: {}".format(e))
        log_resp_time(logger, "load_postgresdb", timer)

    def inspect_postgresqldb(self):
        logger.info("{} UwAccount loaded into Postgres DB".format(
            len(UwAccount.objects.all())))

    def cleanup(self):
        # Cleanup: Delete the local fixture file
        if os.path.exists(self.fixture_file):
            os.remove(self.fixture_file)
