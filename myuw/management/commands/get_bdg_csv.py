# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import html
import logging
import csv
import os
import json
import re
from django.core.management.base import BaseCommand
from restclients_core.exceptions import DataFailureException
from uw_space import Facilities

logger = logging.getLogger(__name__)


class UWFacilities(Facilities):
    def search_by_name(self, facility_name):
        """
        facility_code: string
        """
        url = f"/space/v2/facility.json?long_name={facility_name}"
        response = self.dao.getURL(url, self._read_headers)
        logger.debug(
            {"url": url, "status": response.status, "data": response.data})
        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        return self.__process_json(json.loads(response.data))


def get_building_data():
    dao = UWFacilities()
    buildings = []
    data_file = os.path.join(
        os.path.join(os.path.dirname(__file__), "../../", "data"),
        "campus_map_buildings.csv")
    reader = csv.reader(
        open(data_file, "r", encoding="utf8"), delimiter=",")
    next(reader)  # skip header
    for line in reader:
        try:
            s = re.match(r"^(.*)\(([^()]+)\)\s*$", line[0])
            if not s:
                continue
            name = s.group(1).rstrip()
            code = s.group(2).strip()
            logger.info(f"{name}, {code}\n")
            fac = None
            if code and len(code):
                try:
                    fac = dao.search_by_code(code)
                except Exception as ex:
                    logger.error(f"{ex} with {name}, {code}")
            if not fac:
                try:
                    fac = dao.search_by_name(name)
                except Exception as ex:
                    logger.error(f"{ex} with {name}, {code}")
            if fac:
                buildings.append(fac)
        except Exception as ex:
            logger.error(f"{ex} with name in line: {line}")
    return buildings


class Command(BaseCommand):

    def handle(self, *args, **options):
        building_data = get_building_data()
        if building_data and len(building_data) > 0:
            try:
                with open(
                    "./upd_buildings.csv", "w", newline="", encoding="utf-8"
                ) as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        ["Campus location Name", "Map link", "Address"])
                    for fac in building_data:
                        bname = html.escape(fac.name)
                        writer.writerow(
                            [
                                f"{fac.name} ({fac.code})",
                                (f"\"https://maps.google.com/maps?q={bname}@" +
                                    f"{fac.latitude},{fac.longitude}&z=18\""),
                                f"\"{fac.latitude},{fac.longitude}\""
                            ])
            except Exception as ex:
                logger.error(ex)
