# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_space import Facilities
from myuw.models import CampusBuilding
from myuw.test.api import MyuwApiTest


class TestBuilding(MyuwApiTest):
    def test_building(self):
        fac_obj = Facilities().search_by_number("1347")
        b_obj = CampusBuilding.upd_building(fac_obj)
        self.assertEqual(b_obj.latitude, 47.6536929997)
        self.assertEqual(b_obj.longitude, -122.304747)
        self.assertEqual(b_obj.name, "Mechanical Engineering Building")
        self.assertEqual(b_obj.code, 'MEB')
        self.assertEqual(b_obj.number, '1347')
        self.assertEqual(
            b_obj.json_data(),
            {
                'code': 'MEB',
                'latitude': 47.6536929997,
                'longitude': -122.304747,
                'name': 'Mechanical Engineering Building',
                'number': '1347',
            }
        )
        self.assertIsNotNone(str(b_obj))

        obj1 = CampusBuilding.get_building_by_code('MEB')
        self.assertEqual(
            obj1.json_data(),
            {
                'code': 'MEB',
                'latitude': '47.6536929997',
                'longitude': '-122.304747',
                'name': 'Mechanical Engineering Building',
                'number': '1347',
            }
        )

        obj2 = CampusBuilding.get_building_by_number('1347')
        self.assertEqual(
            obj2.json_data(),
            {
                'code': 'MEB',
                'latitude': '47.6536929997',
                'longitude': '-122.304747',
                'name': 'Mechanical Engineering Building',
                'number': '1347',
            }
        )

        self.assertTrue(CampusBuilding.exists('MEB'))
        self.assertTrue(CampusBuilding.exists_by_number('1347'))

        fac_obj.code = 'MEBB'
        obj3 = CampusBuilding.upd_building(fac_obj)
        self.assertEqual(obj3.code, 'MEBB')
        self.assertFalse(b_obj == obj3)
