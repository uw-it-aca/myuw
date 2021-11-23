# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from uw_space import Facilities
from myuw.models import CampusBuilding
from myuw.logger.logresp import log_info
from myuw.dao import is_using_file_dao, log_err

logger = logging.getLogger(__name__)
space = Facilities()


def get_building_by_code(building_code):
    if (building_code is None or
            building_code == "*" or len(building_code) < 1):
        return None
    try:
        if CampusBuilding.exists(building_code):
            # in local data store
            return CampusBuilding.get_building_by_code(building_code)

        log_info(
            logger,
            {'msg': "get_building_by_code({}) Not in DB".format(
                building_code)})

        fac_objs = space.search_by_code(
            'MEB' if is_using_file_dao() else building_code)

        if len(fac_objs) == 0:
            logger.error(
                {'msg': "get_building_by_code({}) Invalid code!".format(
                    building_code)})
            return None

        fac_obj = fac_objs[0]
        if is_using_file_dao():
            fac_obj.code = building_code

        return CampusBuilding.upd_building(fac_obj)
    except Exception:
        log_err(logger, "get_building_by_code({})".format(
            building_code), traceback, None)
    return None


def get_buildings_by_schedule(schedule):
    """
    Returns a dictionary is build-code and Building model
    for the given class schedule. Return None if the schedule
    contains no section.
    """
    buildings = {}

    for section in schedule.sections:
        if section.final_exam and section.final_exam.building:
            code = section.final_exam.building
            if code not in buildings:
                buildings[code] = get_building_by_code(code)

        for meeting in section.meetings:
            if not meeting.building_to_be_arranged:
                code = meeting.building
                if code not in buildings:
                    buildings[code] = get_building_by_code(code)

    return buildings
