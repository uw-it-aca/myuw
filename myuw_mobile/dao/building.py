"""
This module gives access to building data
"""
import json
import os
from myuw_mobile.models.building import Building


def get_building_by_code(code):
    """
    Returns a Building model for the given code, or None
    """
    path = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'buildings.json')

    f = open(path)
    building_data = json.loads(f.read())

    if code in building_data:
        data = building_data[code]
        building = Building()
        building.longitude = data["longitude"]
        building.latitude = data["latitude"]
        building.name = data["name"]

        return building


def get_buildings_by_schedule(schedule):
    """
    Returns a dictionary is build-code and Building model
    for the given class schedule. Return None if the schedule
    contains no section.
    """
    if schedule is None or len(schedule.sections) == 0:
        return None
    buildings = {}
    for section in schedule.sections:
        if section.final_exam and section.final_exam.building:
            code = section.final_exam.building
            if code not in buildings:
                building = get_building_by_code(code)
                buildings[code] = building

        for meeting in section.meetings:
            if not meeting.building_to_be_arranged:
                if meeting.building not in buildings:
                    code = meeting.building
                    building = get_building_by_code(code)
                    buildings[code] = building

    return buildings
