# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from myuw.models import CampusBuilding
import logging
import csv

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed campus_building.location_url from a crosswalk CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path",
                            help="CSV file containing map urls")
        parser.add_argument("-c", "--commit", action="store_true",
                            dest="commit", default=False,
                            help="Update building models with map urls")

    def handle(self, *args, **options):
        file_path = options.get("file_path")
        commit = options.get("commit")

        building_lookup = {}
        with open(file_path, "r") as infile:
            for row in csv.reader(infile):
                if not len(row):
                    continue

                building_code = row[1].strip()
                map_url = row[6].strip()

                if building_code and map_url:
                    building_lookup[building_code] = map_url

        for building in CampusBuilding.objects.all():
            map_url = building_lookup.get(building.code)
            if map_url:
                logger.info(f"Found map_url for building {building.code}")
                building.location_url = map_url
                if commit:
                    building.save()
                    logger.info(
                        f"Updated location_url for building {building.code}")
