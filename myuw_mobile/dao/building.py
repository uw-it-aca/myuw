import json
import os
from myuw_mobile.models import Building

class Building:
    """ This class gives access to building data """

    def get_building_from_code(self, code):
        """ Returns a Building model for the given code, or None """
        path = os.path.join(
                            os.path.dirname( __file__ ),
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
