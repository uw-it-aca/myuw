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
model_list = [
    'myuw.BannerMessage',
    'myuw.CampusBuilding',
    'myuw.MyuwNotice',
    'myuw.PopularLink',
    'myuw.ResCategoryLink',
    'myuw.CustomLink',
    'myuw.HiddenLink',
    'myuw.Instructor',
    'myuw.MigrationPreference',
    'myuw.ResourceCategoryPin',
    'myuw.SeenRegistration',
    'myuw.UserCourseDisplay',
    'myuw.UserNotices',
    'myuw.VisitedLinkNew',
    'PersistentMessageMessage',
    'PersistentMessageTaggroup',
    'PersistentMessageTag',
    'PersistentMessageMessageTags'
]
user_model = 'myuw.User'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'action', choices=[
                'dump', 'load', 'tidy'
            ]
        )

    def handle(self, *args, **options):
        if self.action == 'dump':
            self.dump_mysql_data()
        if self.action == 'load':
            self.load_postgresdb()
        if self.action == 'tidy':
            self.cleanup()

    def dump_mysql_data(self):
        self.fixture_files = []
        for model_name in model_list.append(user_model):
            self.prep(model_name)
            fixture_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "mysql_{}_data_fixture.json".format(model_name.lower()))
            logger.info("Start dumping {} to {}".format(
                model_name, fixture_file))
            self.dump_amodel(model_name, fixture_file)

    def load_postgresdb(self):
        for model_name in [user_model] + model_list:
            fixture_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "mysql_{}_data_fixture.json".format(model_name.lower()))
            logger.info("Start loading {} from {}".format(
                model_name, fixture_file))
            self.load_amodel(model_name, fixture_file)
            self.inspect_postgresqldb(model_name)

    def prep(self, model_name):
        logger.info("{} {} in mysql DB".format(
            model_name,
            model_name.objects.using('mysql').all().count()))

    def dump_amodel(self, model_name, fixture_file):
        timer = Timer()
        try:
            model_list = [model_name]
            call_command(
                'dumpdata', *model_list, '--database=mysql',
                output=fixture_file)
        except CommandError as e:
            logger.error(
                "Dump {} from the MySQL DB: {}".format(
                    model_name, e))
        log_resp_time(logger, "dump_mysql_data {}".format(
            model_name), timer)

    def load_amodel(self, model_name, fixture_file):
        timer = Timer()
        try:
            call_command('loaddata', fixture_file)
        except CommandError as e:
            logger.error(
                "Load data into Postgres DB: {}".format(
                    model_name, e))
        log_resp_time(logger, "load_postgresdb{}".format(
            model_name), timer)

    def inspect_postgresqldb(self, model_name):
        logger.info("{} UwAccount loaded into Postgres DB".format(
            model_name.objects.all().count()))

    def cleanup(self):
        # Cleanup: Delete the local fixture file
        for model_name in [user_model] + model_list:
            fixture_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "mysql_{}_data_fixture.json".format(model_name.lower()))
            if os.path.exists(fixture_file):
                logger.info("Delete {}".format(fixture_file))
                os.remove(fixture_file)
