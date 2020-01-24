import logging
import os
from django.core.management.base import BaseCommand, CommandError
from uw_gws import GWS
from myuw.dao import _get_file_path

gws = GWS()
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('group_id', type=str,
                            help="param1: group_id")
        parser.add_argument('file_name', type=str,
                            help="param2: file_name")

    def handle(self, *args, **options):
        counter = 0
        group_id = options['group_id']
        file_name = options['file_name']
        file_path = _get_file_path("MYUW_DATA_PATH", file_name)
        with open(file_path, 'r', encoding='utf8') as data_source:
            for line in data_source:
                try:
                    netid = line.rstrip()
                    if netid == "uw_netid":
                        continue
                    gws.add_members(group_id, netid)
                    counter += 1
                except Exception as ex:
                    logger.error("{}: {}".format(str(ex), line))
        logger.info("Added {} members".format(counter))
